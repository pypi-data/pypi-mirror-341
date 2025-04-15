# Exploring LLM Priming Strategies for Few-Shot Stance Classification

How does priming affect prompt-based learing?
This project aims at analyzing this effect in stance classification.
We train a stance classifier on the ibm stance classification dataset by
fine-tuning an Alpaca model with a prompt and analyzing how does the selection
of the few shots used in the prompt affect the performance of the model.

1) To evaluate the prompt-fine-tuning, run the following command
* Hyperparamter optimization
```
python scripts/run_prompt_fine_tuning.py --validate --optimize 
```

* T evaluate the prompt fine-utning approach using best hyperparameters in the config file.
```
python scripts/run_prompt_fine_tuning.py --validate  
``` 
2) To evaluate the prompting approaches (prompt) setup run
```
python scripts/run_prompting.py --validate --optimize 
```
3) To optmize DeBERTa using the hyperparameters in the config file, run the following
```
python scripts/optimize_baseline.py 
```
4) run the majority baseline
```
 python baseline.py --vast --majority --offline
```
5) Run prompting or prompt-fine tuning approaches with anaylze k as folows
```
python scripts/run_prompt_fine_tuning.py --analyze-k  
``` 


The ks or topic-counts are stored in [conf.yaml](conf) and the analysis will be run for multiple seeds and the
performance will be averaged and saved in the corresponding entry in /bigwork/nhwpajjy.
To perform an analysis for one k  instnance you can give it as a parameter using --k 
to produce the results for one seed you can specify the seed using --seed

2. Store the path of the produced csv file in [conf.yaml](conf.yaml) under `` analyze-k ``


The results of the experiments will be logged to your home directory.
The parameters can be saved in [config.yaml](../blob/maser/config.yaml)

## Priming Sampling strategies
To run an experiment with a priming sampling strategy use the parameter ```--similar-examples```. This will retrieve
priming examples tailored toward the test instance. The priming examples are selected using Sentence-Transformers ```--sentence-transformer```.
Example,

```python scripts/run_prompting.py --validate --topic-similar --sentence-transformer```


To run an experiment with a diversification sampling strategy use the parameter ```--diverse-examples```. This
will takes precomputed cluster centers of the training set as few shots. The number of clusters is then the few shot count
provided in the configuration.
## Topic Priming
Topic-priming examples are sampled using a topic similarity, which relies on sentence transformer. 
the similarities can be used to apply the right sampling strategy.

1) To compute the similarities between all the validation and training arguments run the following
```
python scripts/run_develop_similarity_measure.py --compute-similarity --ibmsc
```
You have to specify the model used to compute the similarity to be ```--sentence-transformer``` 

To load similarities from the code you can use the

```similarities = load_similarities("ibmsc", "validation", similarity)```

which returns a dictionary of dictionary where the indices of the first dictionary are the test indices and the indeices
of the nested dictionary for each test index are the indices of the training set with the values being the similarity scores.

To find similar or diverse arguments for an argument in the validation or test set, you can use

```examples = sample_diverse_examples(experiment, experiment_type, few_shot_size)```

similar can be used for sample_similar

```examples = sample_similar_examples(test_istance_index, similarities, df_training, few_shot_size)```

Similar examples for alll datasets are cached for efficiency and can be created by running the following commands

```
python argument_sampling/sampling_strategies.py" --ibmsc
```

to generate similar examples while using percentiles similarity thresholds you can use 
```
python argument_sampling/sampling_strategies.py" "--ibmsc" --percentiles 10
```

## Stance Priming

Stance-priming approaches use stance similarity to retrieve examples with similar stance to an input instance. To train
the contrastive similarity measure, run 
```
python scripts/traing_contrastive_learning.py --vast --lr --epochs --batch-size --output-path-model  
```
The best parameters are also saved in the config file, which will be used as default for each dataset. 

To optimize the contrastive similarity measure on the validation set using the hyperparamters in the  script, run.
```
python scripts/traing_contrastive_learning.py --vast --optimize  --results-path "$DATA_PATH/contrastive_learning/models/optimization-contrastive-learning-ibmsc.tsv"
```
To generate the similarity matrix using the contrastive similarity measure use 
```
python scripts/generate_stance_priming_samples.py --vast --similarity-matrix 
```

To generate the stance priming samples using most similar , run the following 
```
python scripts/generate_stance_priming_samples.py --vast --different-topics 
```

to generate similar examples while using percentiles similarity thresholds you can use
```
python scripts/generate_stance_priming_samples.py" "--ibmsc" --percentiles 10 --different-topics
```


## Diversification strategy

To sample diverse examples, we use ward hierarchical clustering algorithm to cluster the trianing examples into $k$ cluster.
The center of each cluster is then taken as an example. To find the diverse examples, we use the following command


```
python scripts/run_sample_diverse_examples --vast --validate --ibmsc 
```
This will precompute the cluster centers for k in  ```[2, 4, 8, 16, 32, 64]```
To sample diverse examples, you can use the following command

```examples = sample_diverse_examples(experiment, experiment_type, few_shot_size)``` where experiment is ibmsc or vast
and experiment_type is validation or test.

## Analysis

Mainly there are three types of analyses implemented on the prompting and instruction fine-tuning approaches.
For this the results for all ks and the specific model and counts should be in the config file
### Few shot size or training topic count effect on priming approaches


```
python script/run_visualize_over_k_performance.py --k --prompting --prompt-fine-tuning
```

2. Run the signifance tests. For this you need to store the predictions of the models using --path-predictions for all seeds
```
python notebooks/signifiance_test.py
```

3. Run the prime anaylis for stance priming you can run

```
 python "$CODE_PATH/scripts/run_prompting.py"  "--alpaca-7b" "--ibmsc" --offline --vllm --analyze-prime-similarity  \
 --similar-examples --path-similar-examples "$DATA_PATH/sampling-strategies/ibmsc-similar-stance-examples.tsv"
```

3. Run the prime anaylis for topic priming you can run

```
 python "$CODE_PATH/scripts/run_prompting.py"  "--alpaca-7b" "--ibmsc" --offline --vllm --analyze-topic-similarity  \
 --similar-examples --path-similar-examples "$DATA_PATH/sampling-strategies/ibmsc-similar-stance-examples.tsv"
```
