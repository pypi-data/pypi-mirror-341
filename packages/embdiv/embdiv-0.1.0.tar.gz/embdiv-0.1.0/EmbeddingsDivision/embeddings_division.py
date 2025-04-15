import gc
import torch
import transformers
import torch.nn as nn
from cachetools import Cache
from typing import List, Optional, Union


class EmbeddingsDivision():
    def __init__(self, model_name, device='cpu'):
        """
        Initializes the instance using a pretrained model configuration and architecture,
        loads the corresponding model, and moves it to the specified computation device.

        Args:
            model_name (str): The name or path to the pretrained model. This argument is
                passed to the transformers library to load the associated configuration
                and architecture.
            device (str, optional): The computation device to which the model is moved.
                Defaults to 'cpu'.
        """

        config = transformers.AutoConfig.from_pretrained(model_name)
        model_type = [
            arch for arch in config.architectures if arch.endswith('LM')][0]

        try:
            self.model = self.create_inner_model(
                getattr(transformers, model_type), model_name)
            self.forward_change()
            
            
        except Exception as e:
            self.model = self.create_tuned_model(
                getattr(transformers, "LlamaForCausalLM"), model_name)
        
        self.device = device

    def scheduler_hook(self, grad, row):
        if self.training == True:
            if self.model.forward_passes % 10 == 0:
                grad[row] = 0
            
        return grad
    
    def create_tuned_model(self, model_class: transformers.AutoModelForCausalLM, model_name: str):
        """
        Generates a specialized model class by inheriting from the specified base model and
        initializes it with the provided model name. The resulting model is loaded with
        pretrained weights via the from_pretrained method.

        Args:
            model_class (AutoModelForCausalLM): The Hugging Face model class to be extended.
            model_name (str): The name or path of the pretrained model.
        Returns:
            AutoModelForCausalLM: An instance of the custom model class with loaded weights.
        """

        class ModelForCausalLM(model_class):
            def __init__(self, model_name):
                super().__init__(model_name)
                self.model.embed_tokens1 = nn.Embedding(85629, 2048)
                self.model.embed_tokens2 = nn.Embedding(42627, 2048)

        model = ModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.bfloat16)
        
        model.model.embed_tokens.weight.data[:85629] = model.model.embed_tokens1.weight.data
        model.model.embed_tokens.weight.data[85629:] = model.model.embed_tokens2.weight.data

        return model

    def create_inner_model(self, model_class: transformers.AutoModelForCausalLM, model_name: str):
        """
        Generates a specialized model class by inheriting from the specified base model and
        initializes it with the provided model name. The resulting model is loaded with
        pretrained weights via the from_pretrained method.

        Args:
            model_class (AutoModelForCausalLM): The Hugging Face model class to be extended.
            model_name (str): The name or path of the pretrained model.
        Returns:
            AutoModelForCausalLM: An instance of the custom model class with loaded weights.
        """

        class ModelForCausalLM(model_class):
            def __init__(self, model_name):
                super().__init__(model_name)

        model = ModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.bfloat16)
        
        return model
    
    def divide_embeddings(self, ratio: float):
        """
        Splits the model's embedding layer into two new embedding layers, each sized
        according to the specified ratio of the original vocabulary size.

        Args:
            ratio (float): A floating-point value between 0 and 1, indicating the
                proportion of the vocabulary allocated to the first embedding layer.

        Raises:
            ValueError: If the ratio is not strictly between 0 and 1.

        This method replaces the original embedding layer with two new embedding
        layers, transfers the corresponding weight data from the original embedding
        to each of the new layers, and updates the model's forward pass. The original
        embedding layer is deleted afterward to free resources.
        """

        if ratio <= 0 or ratio >= 1:
            raise ValueError("Ratio must be between 0 and 1")

        vocab_size = self.model.model.config.vocab_size

        first_embedding = nn.Embedding(
            round(vocab_size * ratio), self.model.model.config.hidden_size)
        second_embedding = nn.Embedding(
            round(vocab_size * (1 - ratio)), self.model.model.config.hidden_size)
        
        # set the hook to the first embedding
        # first_embedding.weight.register_hook(lambda grad: self.scheduler_hook(grad, i) for i in range(first_embedding.weight.size(0)))

        first_embedding.weight.data.copy_(
            self.model.model.embed_tokens.weight.data[:round(vocab_size * ratio)])
        second_embedding.weight.data.copy_(
            self.model.model.embed_tokens.weight.data[vocab_size - round(vocab_size * (1 - ratio)):])

        first_embedding.to(self.device)
        second_embedding.to(self.device)

        setattr(self.model.model, 'embed_tokens1', first_embedding)
        setattr(self.model.model, 'embed_tokens2', second_embedding)
        setattr(self.model, 'forward_passes', 0)

        del self.model.model.embed_tokens

        self.forward_change()
        gc.collect()

    def forward_change(self):
        setattr(self.model, 'forward_passes', 0)
        self.model.original_forward = self.model.forward
        self.model.forward = self.modified_forward

    def original_forward(self, *args, **kwargs):
        pass

    def modified_forward(
        self,
        input_ids: torch.LongTensor = None,
        attention_mask: Optional[torch.Tensor] = None,
        position_ids: Optional[torch.LongTensor] = None,
        past_key_values: Optional[Union[Cache, List[torch.FloatTensor]]] = None,
        inputs_embeds: Optional[torch.FloatTensor] = None,
        labels: Optional[torch.LongTensor] = None,
        use_cache: Optional[bool] = None,
        output_attentions: Optional[bool] = None,
        output_hidden_states: Optional[bool] = None,
        return_dict: Optional[bool] = None,
        cache_position: Optional[torch.LongTensor] = None,
        num_logits_to_keep: int = 0,
        **kwargs
    ):
        if input_ids is None and inputs_embeds is None:
            raise ValueError(
                "You have to specify either input_ids or inputs_embeds")

        mask = input_ids > self.model.model.embed_tokens1.num_embeddings

        pretrained_batch = input_ids.clone()
        pretrained_batch[mask] = 0

        inputs_embeds = self.model.model.embed_tokens1(pretrained_batch)

        input_ids -= self.model.model.embed_tokens1.num_embeddings

        input_ids[~mask] = 0
        non_pretrained_embedded_batch = self.model.model.embed_tokens2(
            input_ids)

        inputs_embeds[mask] = non_pretrained_embedded_batch[mask]

        input_ids = None
        
        # print(inputs_embeds)
        if self.model.training == True:
            self.model.forward_passes += 1
        
        print("========================================")
        print(inputs_embeds)
        print("========================================")

        return self.original_forward(
            input_ids=input_ids,
            attention_mask=attention_mask,
            position_ids=position_ids,
            past_key_values=past_key_values,
            inputs_embeds=inputs_embeds,
            use_cache=use_cache,
            output_attentions=output_attentions,
            output_hidden_states=output_hidden_states,
            return_dict=return_dict,
            cache_position=cache_position,
            labels=labels,
            num_logits_to_keep=num_logits_to_keep,
            **kwargs
        )
