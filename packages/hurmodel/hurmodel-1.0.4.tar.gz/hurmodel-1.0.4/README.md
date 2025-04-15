HurModel is a new and sophisticated architecture for GPT-type language models that relies on the abstraction of simplified features of the HurNet neural network.

# HurModel

The HurModel (with “Hur” from “HurNet” and “Model” from language model) is a revolutionary new architecture for Transformer-based language models that can be characterized as a new kind of GPT model. The algorithm introduces a new paradigm in which a simplified abstraction of the HurNet neural network is used for the intelligent initialization of deterministic weights, for the insertion of optimization layers, and for the auxiliary tuning of the final weights. The main class features a basic construction of an HurNet artificial neural network where only the pseudo-inverse computations with activation functions are abstracted and encoded on resources of a PyTorch module used for GPU hardware acceleration. In this way, only the aspects of greater speed of the HurNet network are employed to ensure maximum performance during data transitions between conventional Transformer networks and Transformer networks with HurNet—and vice versa. Due to the simplification of the traditional HurNet network into a PyTorch-based HurNet network, we have named the new architecture HurNetTorch. The HurModel algorithm also features automatic and intelligent hyperparameter parametrization, eliminating the need for developers to manually adjust configurations. All of this makes the HurModel much faster, more dynamic, accurate, and efficient than traditional GPT models, while also allowing for simpler and more straightforward development.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the Hur Model.

```bash
pip install hurmodel
```

## Usage
Basic usage example:
```python
from hurmodel import HurModel # importing the main class from the module
hurmodel = HurModel() # instantiation of the main class object
# the "addFit" method takes an input sample in the first argument and a desired output for this sample in the second argument
# when the "addFit" method is called before the "train" method, it adds the input and output pairs to the dataset for training
# if the dataset is empty, the input pairs of the "addFit" method will become the dataset itself
# if the dataset has content, the input and output pairs will be added as an addendum at the end of the dataset
# if the "addFit" method is invoked after training, the sample pairs will be adjusted as a fine-tuning on top of the base model that has already been trained
# the "prompt" argument receives an question example, instruction, or sample of input
# the "answer" argument receives an example answer or sample of output for the input of the same method invocation
# the "addFit" method can be invoked/called as many times as necessary depending on the size of your training dataset
hurmodel.addFit(prompt='What does the acronym GPT mean in language models?', answer='GPT in language models stands for Generative Pre-trained Transformer.') # always use string values in "prompt" and "answer"
hurmodel.addFit(prompt='What is the capital of Spain?', answer='The capital of Spain is Madrid.') # returns True if the addition is successful or False otherwise
hurmodel.train() # the "train" method trains the model with the previously added data
# the "predict" function returns a text with the answer to the input received in the "prompt" argument
# the answer will always be based on the most likely output sample for the input of prediction
# to calculate the response, a probabilistic search will be performed on the pairs added with "addFit" to find the pair that has the training input most similar to the prediction input
# the pair that has the training input closest to the input of the "predict" function will have its response used as the basis for constructing the inference response
answer = hurmodel.predict(prompt='what does gpt mean in language models?') # returns a string with the result of the inference (always use string values in "prompt")
print(answer) # displays the inference result

```
Prediction response:
During the training progress, you can view the total number of tokens used to train the model, the total number of resulting parameters, and the HurNet network configuration status.
When viewing the HurNet network configurations, you can view in "Init" whether the intelligent initialization of weights was used, in "Layer" you can view whether any layer of the HurNet network was added to the Transformer network layering architecture, and in "Fit" you can view whether the auxiliary adjustment of weights of the HurNet network is being applied to the training.
You can also view the percentage (between 0 and 1) of information loss and the final training "precision" with values between 0 and 1 estimated based on how much the network learned.
```bash
Training [52/tokens, 12M/params] - HurNet: [Init: ON, Layer: OFF, Fit: OFF]: 1890it [00:09, 193.07it/s, loss=0.0163, precision=0.984]                           
GPT in language models stands for Generative Pre-trained Transformer.
```
Here's another basic example with more input and output samples. The more question variations per answer you add, the lower your chances of error in inference.
```python
# note how building language models with the hurmodel architecture is much simpler and more objective than if you were using any other module for transformers
from hurmodel import HurModel
hurmodel = HurModel()
# we recommend that you use different questions for the same answer, this way you will reduce the chances of error in the inference answers
hurmodel.addFit(prompt='What does the acronym GPT mean in language models?', answer='GPT in language models stands for Generative Pre-trained Transformer.')
hurmodel.addFit(prompt='Tell me what is the meaning of GPT in language models.', answer='GPT in language models stands for Generative Pre-trained Transformer.')
hurmodel.addFit(prompt='What is the capital of Spain?', answer='The capital of Spain is Madrid.')
hurmodel.addFit(prompt='Tell me the name of the capital of Spain.', answer='The capital of Spain is Madrid.')
hurmodel.train(progress=False) # set False to the "progress" parameter if you want to hide the training progress (the default value is True)

answer = hurmodel.predict(prompt='What is the capital of Spain?')
print(answer)

```
Prediction response:
```bash
The capital of Spain is Madrid.
```
It is not recommended to train the model every time you want to infer an answer, as this will make the inference process slow and painful. To avoid this, we use the "saveModel" method to train the model only once and reuse the pre-trained model in future inferences. The "saveModel" method will save a file in GPT format in any directory of your choice.
```python
from hurmodel import HurModel
hurmodel = HurModel()
# data creation for the training dataset
hurmodel.addFit(prompt='What does the acronym GPT mean in language models?', answer='GPT in language models stands for Generative Pre-trained Transformer.')
hurmodel.addFit(prompt='Tell me what is the meaning of GPT in language models.', answer='GPT in language models stands for Generative Pre-trained Transformer.')
hurmodel.addFit(prompt='What is the capital of Spain?', answer='The capital of Spain is Madrid.')
hurmodel.addFit(prompt='Tell me the name of the capital of Spain.', answer='The capital of Spain is Madrid.')
# training of model
hurmodel.train()
# saving the trained model, if no name is specified for the model file, the model will be saved with the name "model.gpt" in the local directory
hurmodel.saveModel()

```
```bash
Training [111/tokens, 13M/params] - HurNet: [Init: ON, Layer: OFF, Fit: OFF]: 4200it [00:22, 189.45it/s, loss=0.00736, precision=0.993]
```
Use the method named 'loadModel' if you want to load a pre-trained model for a faster inference.
```python
from hurmodel import HurModel
hurmodel = HurModel()
# there is no need to waste time on retraining if you are loading a model that has already been pre-trained and saved previously
hurmodel.loadModel() # if no model file name is specified, the method will look in the local directory for a model with default name, in this case with the name "model.gpt"
# with the pre-loaded template, simply ask any question about the data contained in this template
answer = hurmodel.predict(prompt='what is the capital of spain?')
print(answer)

```
```bash
The capital of Spain is Madrid.
```
Now see how to define a name for your saved model.
```python
from hurmodel import HurModel
hurmodel = HurModel()

hurmodel.addFit(prompt='What does the acronym GPT mean in language models?', answer='GPT in language models stands for Generative Pre-trained Transformer.')
hurmodel.addFit(prompt='Tell me what is the meaning of GPT in language models.', answer='GPT in language models stands for Generative Pre-trained Transformer.')
hurmodel.addFit(prompt='What is the capital of Spain?', answer='The capital of Spain is Madrid.')
hurmodel.addFit(prompt='Tell me the name of the capital of Spain.', answer='The capital of Spain is Madrid.')

hurmodel.train()
# use the "model_path" parameter if you want to specify a path and/or name for your model
hurmodel.saveModel(model_path='my_model.gpt') # the ".gpt" extension is optional as it will be automatically added to the end of the file name

```
```bash
Training [111/tokens, 13M/params] - HurNet: [Init: ON, Layer: OFF, Fit: OFF]: 4200it [00:22, 187.47it/s, loss=0.0036, precision=0.996]
```
Now just use the loading method to load the model that was pre-trained earlier.
```python
from hurmodel import HurModel
hurmodel = HurModel()
# use the "model_path" parameter if you want to specify a path and/or name for your model
hurmodel.loadModel(model_path='my_model.gpt') # the ".gpt" extension is optional as it will be automatically added to the end of the file name

answer = hurmodel.predict(prompt='what is the capital of spain?')
print(answer)

```
```bash
The capital of Spain is Madrid.
```
You can also specify a path to save your template. If the specified path does not exist, it will be automatically created.
```python
from hurmodel import HurModel
hurmodel = HurModel()

hurmodel.addFit(prompt='What does the acronym GPT mean in language models?', answer='GPT in language models stands for Generative Pre-trained Transformer.')
hurmodel.addFit(prompt='Tell me what is the meaning of GPT in language models.', answer='GPT in language models stands for Generative Pre-trained Transformer.')
hurmodel.addFit(prompt='What is the capital of Spain?', answer='The capital of Spain is Madrid.')
hurmodel.addFit(prompt='Tell me the name of the capital of Spain.', answer='The capital of Spain is Madrid.')

hurmodel.train()

hurmodel.saveModel(model_path='./models/my_model.gpt')

```
```bash
Training [111/tokens, 13M/params] - HurNet: [Init: ON, Layer: OFF, Fit: OFF]: 4200it [00:22, 187.69it/s, loss=0.00678, precision=0.993]
```
After just specify the same path in the "loadModel" method.
```python
from hurmodel import HurModel
hurmodel = HurModel()

hurmodel.loadModel(model_path='./models/my_model.gpt')

answer = hurmodel.predict(prompt='what is the capital of spain?')
print(answer)

```
```bash
The capital of Spain is Madrid.
```
Instead of calling the "addFit" method multiple times, you can just call the "train" method once, passing a string with all the training data.
```python
from hurmodel import HurModel
hurmodel = HurModel()
# string variable containing the text that will be used in training the model
string = '''
What does the acronym GPT mean in language models?
GPT in language models stands for Generative Pre-trained Transformer.

Tell me what is the meaning of GPT in language models.
GPT in language models stands for Generative Pre-trained Transformer.

What is the capital of Spain?
The capital of Spain is Madrid.

Tell me the name of the capital of Spain.
The capital of Spain is Madrid.
'''
# use the "string" name parameter contained in the "train" method to train the model with all the data at once
hurmodel.train(string=string)
# a model file will be created in the "models" directory with the name "hur_model.gpt"
hurmodel.saveModel(model_path='./models/hur_model') # note that the ".gpt" extension is optional

```
```bash
Training [95/tokens, 13M/params] - HurNet: [Init: ON, Layer: OFF, Fit: OFF]: 3570it [00:18, 189.67it/s, loss=0.0498, precision=0.95]
```
Now loading the previously pretrained model.
```python
from hurmodel import HurModel
hurmodel = HurModel()
# a file named "hur_model.gpt" will be loaded from within the "models" directory
hurmodel.loadModel(model_path='./models/hur_model') # note that the ".gpt" extension is optional

answer = hurmodel.predict(prompt='What is the capital of Spain?')
print(answer)

```
Note that there will be unwanted repetitions in the response returned by the inference. To avoid this we must define a response end tag in our training data.
```bash
The capital of Spain is Madrid.                                                                                                                                 
The capital of Spain is Madrid.
The capital of Spain is Madrid.
The capital of Spain is Madrid.
The capital of Spain is Madrid.
The capital of Spain is Madrid.
The capital of Spain is Madrid.
The capital of Spain is Madrid.
The capital of Spain is Madrid.
The capital of Spain is Madrid.
The capital of Spain is Madrid.
The capital of Spain is Madrid.
The capital of Spain is Madrid.
The capital of Spain is Madrid.
The capital of Spain is Madrid.
The capital of Spain is Madrid.
The capital of Spain is Madrid.
The capital of Spain is Madrid.
The capital of Spain is Madrid.
The capital of Spain is Madrid.
The capital of Spain is Madrid.
The capital of Spain is Madrid.
The capital of Spain is Madrid.
The capital of Spain is Madrid.
The capital of Spain is Madrid.
The capital of Spain is Madrid.
The capital of Spain is Madrid.
The capital of Spain is Madrid.
The capital of Spain is Madrid.
The capital of Spain is Madrid.
The capital of Spain is Madrid.
The capital of Spain is Madrid.
The capital of Spain is Madrid.
The capital of Spain is Madrid.
The capital of Spain is Madrid.
The capital of Spain is Madrid.
The capital of Spain is Madrid.
The capital of Spain is Madrid.
The capital of Spain is Madrid.
The capital of Spain is Madrid.
The capital of Spain is Madrid.
The capital of Spain is Madrid.
The capital of Spain is Madrid.
The capital of Spain is Madrid.
The capital of Spain is Madrid.
The capital of Spain is Madrid.
The capital of Spain is Madrid.
The capital of Spain is Madrid.
The capital of Spain is Madrid.
The capital of Spain is Madrid.
The capital of Spain is Madrid.
The capital of Spain is Madrid.
The capital of Spain is Madrid.
The capital of Spain is Madrid.
The capital of Spain is Madrid.
The capital of Spain is Madrid.
The capital of Spain is Madrid.
The capital of Spain is Madrid.
The capital of Spain is Madrid.
The capital of Spain is Madrid.
The capital of Spain is Madrid.
The capital of Spain is Madrid.
The capital of Spain is Madrid.
```
After each answer, we will define any tag that delimits how far the answer should consult the tokens.
```python
from hurmodel import HurModel
hurmodel = HurModel()
# we chose the tag "<|end|>" to delimiter the end of the answers, but you can create any tag of your choice
# always repeat the same tag after each of the answers
string = '''
What does the acronym GPT mean in language models?
GPT in language models stands for Generative Pre-trained Transformer.
<|end|>
Tell me what is the meaning of GPT in language models.
GPT in language models stands for Generative Pre-trained Transformer.
<|end|>
What is the capital of Spain?
The capital of Spain is Madrid.
<|end|>
Tell me the name of the capital of Spain.
The capital of Spain is Madrid.
<|end|>
'''
# now in training use the "end_tag" parameter so that the method knows which end tag was used in the dataset
# "end_tag" should receive a string with the same tag applied to the dataset above
hurmodel.train(string=string, end_tag='<|end|>')
# set False to the "progress" parameter if you do not want to view the saving progress (the default value is True)
hurmodel.saveModel(model_path='./models/hur_model', progress=False) # the previous template with the same name will be overwritten

```
```bash
Training [116/tokens, 13M/params] - HurNet: [Init: ON, Layer: OFF, Fit: OFF]: 4410it [00:23, 191.38it/s, loss=0.00448, precision=0.996]
```
Now perform a new inference by loading the updated model.
```python
from hurmodel import HurModel
hurmodel = HurModel()
# set False to the "progress" parameter if you do not want to view the loading progress (the default value is True)
hurmodel.loadModel(model_path='./models/hur_model', progress=False)
answer = hurmodel.predict(prompt='What is the capital of Spain?')
print(answer)

```
```bash
The capital of Spain is Madrid.
```
If you prefer, you can also place your end tags to the right of each answer.
```python
from hurmodel import HurModel
hurmodel = HurModel()
# the blank line between one pair and another is not mandatory, but it is recommended
string = '''
What does the acronym GPT mean in language models?
GPT in language models stands for Generative Pre-trained Transformer.<|end|>

Tell me what is the meaning of GPT in language models.
GPT in language models stands for Generative Pre-trained Transformer.<|end|>

What is the capital of Spain?
The capital of Spain is Madrid.<|end|>

Tell me the name of the capital of Spain.
The capital of Spain is Madrid.<|end|>
'''

hurmodel.train(string=string, end_tag='<|end|>')
# it is not necessary to use "./" to refer to the root directory, but it is recommended
hurmodel.saveModel(model_path='models/hur_model.gpt')

```
```bash
Training [111/tokens, 13M/params] - HurNet: [Init: ON, Layer: OFF, Fit: OFF]: 4200it [00:22, 188.17it/s, loss=0.00302, precision=0.997]
```
For loading the model, the structure is the same as we already know.
```python
from hurmodel import HurModel
hurmodel = HurModel()
# it is not necessary to use "./" to refer to the root directory, but it is recommended
hurmodel.loadModel(model_path='models/hur_model.gpt')
answer = hurmodel.predict(prompt='Tell me what is the meaning of GPT in language models.')
print(answer)

```
```bash
GPT in language models stands for Generative Pre-trained Transformer.
```
The best, most reliable and most recommended way to train your model is through a structured file in JSON format.
The vast majority of widely known foundation language models are trained with very well-structured files in JSON format. The training JSON should have a primary key named "data" containing an array with the training data arranged as objects containing a key named "input" for each sample of input/question/instruction and a key named "output" for each desired response. This prevents misinterpretation of the model and increases the degree of accuracy and reliability in the responses.
Example JSON (dataset.json file contents):
```json
{
	"data": [
				{
					"input": "Hello! Who are you?",
					"output": "Hello! I am Sapiens Chat, an AI model created by Sapiens Technology."
				},
				{
					"input": "Who discovered Brazil?",
					"output": "Brazil was discovered by Portuguese navigators led by Pedro Alvares Cabral in 1500."
				},
				{
					"input": "What is the main language spoken in Spain?",
					"output": "The main language spoken in Spain is Spanish."
				},
				{
					"input": "What is the capital of Portugal?",
					"output": "The capital of Portugal is Lisbon."
				},
				{
					"input": "How much is 2 + 2?",
					"output": "The sum of 2 + 2 in mathematics is 4."
				},
				{
					"input": "What is five minus three?",
					"output": "The result of five minus three is two."
				},
				{
					"input": "What is your name?",
					"output": "My name is Sapiens Chat."
				}
	]
}
```
To train your model with a JSON or TXT file, use the parameter named "dataset_path", which should receive a string with the path to your training dataset.
```python
from hurmodel import HurModel
hurmodel = HurModel()
# pass the path of your json or txt file to the value of the "dataset_path" argument
# txt files do not require structuring, although it is highly recommended to use finalization tags in the content of txt files and then define this same tag in the value of "end_tag"
# avoid using files in txt format and always give preference to files structured in json format
hurmodel.train(dataset_path='dataset.json')
# it is not necessary to use "./" to refer to the root directory, but it is recommended
# remember that the ".gpt" extension is also optional, although recommended
hurmodel.saveModel(model_path='models/my_model') # we are using the name "my_model" as an example, but you can give your model any name you want

```
If your model's accuracy is too low, you should increase the size of your dataset.
```bash
Training [196/tokens, 14M/params] - HurNet: [Init: ON, Layer: OFF, Fit: OFF]: 5772it [00:31, 180.72it/s, loss=0.0306, precision=0.969]
```
Now we will test our trained model with the JSON file.
```python
from hurmodel import HurModel
hurmodel = HurModel()
# it is not necessary to use "./" to refer to the root directory, but it is recommended
# remember that the ".gpt" extension is also optional, although recommended
hurmodel.loadModel(model_path='models/my_model')
answer = hurmodel.predict(prompt='What is the capital of Portugal?')
print(answer)

```
```bash
The capital of Portugal is Lisbon.
```
Although not recommended, you can also train your model with a raw, unstructured txt data file.
Example TXT (dataset.txt file contents):
```txt
What is Artificial Intelligence (AI)?
Artificial Intelligence is a field of computer science that develops systems capable of performing tasks that would normally require human intelligence, such as learning, reasoning, perception, and decision-making.

What is the difference between weak AI and strong AI?
Weak AI (or narrow AI) is designed for specific tasks, such as virtual assistants and recommendation systems. Strong AI, on the other hand, would have self-awareness and the ability to understand and reason about any subject like a human being.

What is Machine Learning and how is it related to AI?
Machine Learning is a subfield of AI that teaches machines to learn patterns from data without explicit programming. It allows systems to improve their performance over time with experience.

What are the main types of machine learning?
The three main types are:
- **Supervised Learning**: The model learns from labeled data.
- **Unsupervised Learning**: The model identifies patterns without labels.
- **Reinforcement Learning**: The model learns through trial and error, receiving rewards or penalties.

What are artificial neural networks?
They are models inspired by the functioning of the human brain, composed of layers of artificial neurons that process information and adjust their weights to recognize patterns and make decisions.

What are the risks of Artificial Intelligence?
Some risks include algorithmic bias, job loss due to automation, misuse in surveillance or warfare, and the possibility of superintelligence beyond human control.

How is AI used in everyday life?
AI is present in virtual assistants (Siri, Alexa), recommendation systems (Netflix, Spotify), facial recognition, autonomous cars, medical diagnostics, chatbots, and much more.

What is natural language processing (NLP)?
It is a field of AI that enables machines to understand, interpret, and generate human language, used in machine translation, chatbots, and voice assistants.

Can AI replace humans in the workforce?
AI can automate repetitive and analytical tasks, but it is unlikely to fully replace humans in creative, emotional, and critical thinking jobs.  

What is a generative AI model?
It is a type of AI that can create new content, such as images, text, and music, based on patterns learned from large amounts of data. Examples include ChatGPT and DALL·E.

```
```python
from hurmodel import HurModel
hurmodel = HurModel()

hurmodel.train(dataset_path='dataset.txt')
hurmodel.saveModel(model_path='./models/my_model.gpt')

```
If necessary, retrain your model until your inferences become satisfactory.
```bash
Training [488/tokens, 15M/params] - HurNet: [Init: ON, Layer: OFF, Fit: OFF]: 5888it [00:34, 172.08it/s, loss=0.0078, precision=0.992]
```
Now we can run model inference.
```python
from hurmodel import HurModel
hurmodel = HurModel()
# since "model_path" and "prompt" are the first parameters of their respective functions, their names can be hidden
hurmodel.loadModel('./models/my_model.gpt')
# use the "max_tokens" parameter of the prediction method to set an approximate limit for the total number of tokens in the response
# "max_tokens" must be an integer greater than zero
print(hurmodel.predict('What are the main types of machine learning?', max_tokens=50))

```
```bash
The three main types are:                                                                                                                                       
- **Supervised Learning**: The model learns from labeled data.
- **Unsupervised Learning**: The model identifies patterns without labels.
- **Reinforcement Learning**: The model learns through trial and error, receiving rewards or penalties.
```
To avoid using the "max_tokens" parameter, you can use finalization tags in the content of your TXT file.
Example TXT (dataset.txt file contents):
```txt
What is Artificial Intelligence (AI)?
Artificial Intelligence is a field of computer science that develops systems capable of performing tasks that would normally require human intelligence, such as learning, reasoning, perception, and decision-making.
<|end|>
What is the difference between weak AI and strong AI?
Weak AI (or narrow AI) is designed for specific tasks, such as virtual assistants and recommendation systems. Strong AI, on the other hand, would have self-awareness and the ability to understand and reason about any subject like a human being.
<|end|>
What is Machine Learning and how is it related to AI?
Machine Learning is a subfield of AI that teaches machines to learn patterns from data without explicit programming. It allows systems to improve their performance over time with experience.
<|end|>
What are the main types of machine learning?
The three main types are:
- **Supervised Learning**: The model learns from labeled data.
- **Unsupervised Learning**: The model identifies patterns without labels.
- **Reinforcement Learning**: The model learns through trial and error, receiving rewards or penalties.
<|end|>
What are artificial neural networks?
They are models inspired by the functioning of the human brain, composed of layers of artificial neurons that process information and adjust their weights to recognize patterns and make decisions.
<|end|>
What are the risks of Artificial Intelligence?
Some risks include algorithmic bias, job loss due to automation, misuse in surveillance or warfare, and the possibility of superintelligence beyond human control.
<|end|>
How is AI used in everyday life?
AI is present in virtual assistants (Siri, Alexa), recommendation systems (Netflix, Spotify), facial recognition, autonomous cars, medical diagnostics, chatbots, and much more.
<|end|>
What is natural language processing (NLP)?
It is a field of AI that enables machines to understand, interpret, and generate human language, used in machine translation, chatbots, and voice assistants.
<|end|>
Can AI replace humans in the workforce?
AI can automate repetitive and analytical tasks, but it is unlikely to fully replace humans in creative, emotional, and critical thinking jobs.  
<|end|>
What is a generative AI model?
It is a type of AI that can create new content, such as images, text, and music, based on patterns learned from large amounts of data. Examples include ChatGPT and DALL·E.
<|end|>
```
```python
from hurmodel import HurModel
hurmodel = HurModel()
# since "dataset_path" and "model_path" are the first parameters of their respective functions, their names can be hidden
hurmodel.train('dataset.txt', end_tag='<|end|>')
hurmodel.saveModel('./models/my_model.gpt')

```
Final accuracies above 0.8 are considered highly accurate.
```bash
Training [539/tokens, 16M/params] - HurNet: [Init: ON, Layer: OFF, Fit: OFF]: 5246it [00:31, 166.69it/s, loss=0.00728, precision=0.993]
```
Check below the final result of the inference of the created model.
```python
from hurmodel import HurModel
hurmodel = HurModel()
hurmodel.loadModel('./models/my_model.gpt')
print(hurmodel.predict('What are the main types of machine learning?'))

```
```bash
The three main types are:                                                                                                                                       
- **Supervised Learning**: The model learns from labeled data.
- **Unsupervised Learning**: The model identifies patterns without labels.
- **Reinforcement Learning**: The model learns through trial and error, receiving rewards or penalties.
```
You can also supplement the data in your JSON or TXT dataset with the text from the string parameter.
```python
from hurmodel import HurModel
hurmodel = HurModel()
string = '''
What does the acronym GPT mean in language models?
GPT in language models stands for Generative Pre-trained Transformer.
<|end|>
Tell me what is the meaning of GPT in language models.
GPT in language models stands for Generative Pre-trained Transformer.
<|end|>
What is the capital of Spain?
The capital of Spain is Madrid.
<|end|>
Tell me the name of the capital of Spain.
The capital of Spain is Madrid.
<|end|>
'''
hurmodel.train('dataset.txt', string=string, end_tag='<|end|>')
hurmodel.saveModel('./models/my_model.gpt')

```
The higher the final training accuracy, the lower the variation in responses to a given prompt. The lower the final training accuracy, the higher the variation in responses to a given prompt. Very high accuracies can also cause responses to be very faithful or even identical to the corresponding content in the training dataset. While lower accuracies cause responses to be more different from the corresponding content in the training dataset. The appropriate accuracy will depend on each use case and the specific needs of your project.
```bash
Training [657/tokens, 16M/params] - HurNet: [Init: ON, Layer: OFF, Fit: OFF]: 5070it [00:30, 163.62it/s, loss=0.0126, precision=0.987]
```
Now you can submit related entries, both for the file and the training string value.
```python
from hurmodel import HurModel
hurmodel = HurModel()
hurmodel.loadModel('./models/my_model.gpt')
print(hurmodel.predict('What are artificial neural networks?'))

```
Remember, if your answers are unsatisfactory you must add more data related to the wrong answers to your dataset.
```bash
They are models inspired by the functioning of the human brain, composed of layers of artificial neurons that process information and adjust their weights to recognize patterns and make decisions.
```
The string parameter can also be combined with the contents of a JSON file.
Remember, datasets in JSON format provide much more reliable responses.
```python
from hurmodel import HurModel
hurmodel = HurModel()
dataset_path = './dataset.json'
string = '''
What does the acronym GPT mean in language models?
GPT in language models stands for Generative Pre-trained Transformer.
<|end|>
Tell me what is the meaning of GPT in language models.
GPT in language models stands for Generative Pre-trained Transformer.
<|end|>
What is the capital of Spain?
The capital of Spain is Madrid.
<|end|>
Tell me the name of the capital of Spain.
The capital of Spain is Madrid.
<|end|>
'''
hurmodel.train(dataset_path=dataset_path, string=string, end_tag='<|end|>')
hurmodel.saveModel('./models/my_model.gpt')

```
```bash
Training [286/tokens, 14M/params] - HurNet: [Init: ON, Layer: OFF, Fit: OFF]: 6820it [00:38, 177.74it/s, loss=0.0242, precision=0.976]
```
Check out an inference test below with the model created above.
```python
from hurmodel import HurModel
hurmodel = HurModel()
hurmodel.loadModel('./models/my_model.gpt')
print(hurmodel.predict('Hello! Who are you?'))
print(hurmodel.predict('Tell me what is the meaning of GPT in language models.'))

```
```bash
Hello! I am Sapiens Chat, an AI model created by Sapiens Technology.                                                                                            
GPT in language models stands for Generative Pre-trained Transformer.
```
To fetch one token at a time while each token is generated in real time, set the value of the "stream" parameter to True.
```python
from hurmodel import HurModel
hurmodel = HurModel()
hurmodel.loadModel('./models/my_model.gpt')
# use the "stream" parameter to True if you want to view the token-by-token response as tokens are generated in real time (the default value is False)
generator = hurmodel.predict('Hello! Who are you?', stream=True) # return each token one at a time
for token in generator: # loops through each returned token
    print(token, end='', flush=True) # displays one token in front of another with no space between them
print() # continues terminal execution on the next line

```
Final sequence generated token by token.
```bash
Hello! I am Sapiens Chat, an AI model created by Sapiens Technology.
```
Control the temperature of your responses with the "temperature" parameter.
```python
from hurmodel import HurModel
hurmodel = HurModel()
hurmodel.loadModel('./models/my_model.gpt')
# with the "temperature" parameter you will make the responses more different from each other as the value approaches 1, as well as being able to decrease the variability between one response and another as the value approaches 0 (default value is 0.5 for 50% variation)
generator = hurmodel.predict('What is five minus three?', temperature=0.7, stream=True) # in this case we are defining a variability in the responses of 70%, but this will not always return more varied responses if your final training accuracy was very high
for token in generator: print(token, end='', flush=True)
print()

```
```bash
The result of five minus three is two.
```
Check out an example of a call below with all the prediction parameters and their default values.
```python
from hurmodel import HurModel
hurmodel = HurModel()
hurmodel.loadModel('./models/my_model.gpt')

prompt = 'What is your name?' # input prompt for prediction
# calling the "predict" function with all its parameters and their default values
# note: the default value of the "prompt" parameter is an empty string
answer = hurmodel.predict(prompt=prompt, max_tokens=500, temperature=0.5, stream=False)
print('Question:', prompt) # display the question
print('Answer:', answer) # display the answer

```
```bash
Question: What is your name?                                                                                                                                    
Answer: My name is Sapiens Chat.
```
Use the "print_predict" method to print the prediction response directly to the terminal screen without having to display the result manually.
```python
from hurmodel import HurModel
hurmodel = HurModel()
hurmodel.loadModel('./models/my_model.gpt')
# the "print_predict" method has the same parameters with the same default values as the "predict" method
# note: the default value of the "prompt" parameter is an empty string
hurmodel.print_predict(prompt='Who discovered Brazil?', max_tokens=500, temperature=0.5, stream=False) # prints the answer directly to the screen

```
```bash
Brazil was discovered by Portuguese navigators led by Pedro Alvares Cabral in 1500.
```
Now check out what the display would look like with "stream" enabled.
```python
from hurmodel import HurModel
hurmodel = HurModel()
hurmodel.loadModel('./models/my_model.gpt')
hurmodel.print_predict(prompt='What is the main language spoken in Spain?', stream=True)

```
```bash
The main language spoken in Spain is Spanish.
```
When "end_tag" is set in training, you don't need to worry about the maximum number of tokens in the response.
In this case you can set a high threshold to get a more complete response.
```python
from hurmodel import HurModel
hurmodel = HurModel()
hurmodel.loadModel('./models/my_model.gpt')
# since we defined a responses termination tag in our training, you can use a very high value in "max_tokens" to ensure a complete response and the response will still end at the correct point
hurmodel.print_predict(prompt='What is the capital of Portugal?', max_tokens=1000000, stream=True) # we set one million in "max_tokens" to ensure a complete response (this can only be done when "end_tag" is set in training)

```
```bash
The capital of Portugal is Lisbon.
```
Use the "precision" parameter to set a desired precision for the end of training, thus making your training faster and more dynamic.
```python
from hurmodel import HurModel
hurmodel = HurModel()
# you can control the final precision of your training with a maximum value cutoff, for this use the parameter named "precision"
# the "precision" parameter receives a floating number on a scale between 0 and 1 that represents the percentage of maximum desired precision
# when the training precision is greater than or equal to the precision of the "precision" parameter, the training will be finished with the last precision found
# the default value of the "precision" parameter is 1.0, that is, training will only be completed when the highest possible precision is found, or when the internal adjustment limit is exceeded
# setting "precision" to a value less than 1 will cause the training to complete faster, saving time and processing
# precisions above 0.8 may make your model overfitting and insensitive to adaptations, causing it to lose the ability to generalize to prediction inputs that are very different from the training inputs
# there may be some cases where lower precisions with values close to 0.5 are desirable
hurmodel.train('./dataset.json', precision=0.8) # training will be terminated when accuracy of 0.8 (80%) is reached
hurmodel.saveModel('./models/my_model.gpt')

```
```bash
Training [168/tokens, 14M/params] - HurNet: [Init: ON, Layer: OFF, Fit: OFF]: 3424it [00:08, 409.83it/s, loss=0.137, precision=0.863]
```
```python
from hurmodel import HurModel
hurmodel = HurModel()
hurmodel.loadModel('./models/my_model.gpt')
hurmodel.print_predict(prompt='Hello! Who are you?', stream=True)

```
```bash
Hello! I am Sapiens Chat, an AI model created by Sapiens Technology.
```
With the "tokenizer" parameter you can choose between the Transformers' GPT tokenization pattern that processes pieces of words or Sapiens Technology's SAPI that processes each character individually to increase the level of abstraction in the learning process.
```python
from hurmodel import HurModel
hurmodel = HurModel()
# the "tokenizer" parameter can receive a string with the value "gpt" or with the value "sapi"
# the default value of the tokenizer is "gpt" for a faster but less accurate training
# when setting the tokenizer to "sapi" the training will be a little slower because the knowledge abstraction will be done at the character level and not at the level of pieces of words
# "gpt" tends to be faster and less accurate, while "sapi" tends to be more accurate and less fast
# the choice of tokenizer will depend on your specific case and the needs of your project
hurmodel.train('./dataset.json', tokenizer='sapi', precision=0.9) # the sapi tokenizer should be avoided when training with very small datasets
hurmodel.saveModel('./models/my_model.gpt')
# the sapi tokenizer does not handle very small data sets well, and may return nonsensical responses and repeated characters
# to use the sapi tokenizer on modest datasets, we recommend keeping the precision value higher

```
```bash
Training [573/tokens, 8M/params] - HurNet: [Init: ON, Layer: OFF, Fit: OFF]: 3198it [00:07, 452.04it/s, loss=0.00792, precision=0.992]
```
```python
from hurmodel import HurModel
hurmodel = HurModel()
hurmodel.loadModel('./models/my_model.gpt')
# prefer to set a maximum token limit in models trained with the sapi tokenizer to avoid excessive characters
hurmodel.print_predict(prompt='Who discovered Brazil?', max_tokens=23, stream=True)

```
```bash
Brazil was discovered by Portuguese navigators
```
The "context_window" training parameter is used to set the context window limit for your model. The default value for this parameter is None, but when given an integer greater than zero, your model will use this value as the maximum input token limit for the prompt and the maximum token limit for the context. If "context_window" is left at its default value of None, it will automatically calculate the best value for the context window size based on the current dataset.
```python
from hurmodel import HurModel
hurmodel = HurModel()
# there is no maximum limit for the value of "context_window", but the higher this value is, the slower the training will be and also the slower the inference will be
hurmodel.train('./dataset.json', context_window=1024) # training with 1024 tokens context window
hurmodel.saveModel('./models/my_model.gpt')

```
```bash
Training [168/tokens, 14M/params] - HurNet: [Init: ON, Layer: OFF, Fit: OFF]: 5568it [00:30, 185.47it/s, loss=0.147, precision=0.853]
```
```python
from hurmodel import HurModel
hurmodel = HurModel()
hurmodel.loadModel('./models/my_model.gpt')
# since the model was trained with a context window of 1024 tokens, your prompt will be truncated considering only the final 1024 tokens when the input exceeds this limit
hurmodel.print_predict(prompt='Hello! Who are you?', stream=True) # input must be less than 1025 tokens
```
```bash
Hello! I am Sapiens Chat, an AI model created by Sapiens Technology.
```
The training parameter "hurnet_initializer" enables or disables smart weight initialization using the HurNet network. When set to True, instead of the initial weights being randomly generated as in a conventional neural network, the weights are intelligently initialized with an initial patter recognition, thereby allowing the weights to adjust more quickly and reach the target accuracy in a shorter time. The default value of the "hurnet_initializer" parameter is True, but you can also disable smart weight initialization by setting it to False.
```python
from hurmodel import HurModel
hurmodel = HurModel()
# you will be able to check the status of weights initialization with the hurnet network during the training progress
hurmodel.train('./dataset.json', hurnet_initializer=False) # disabling default initialization of weights
hurmodel.saveModel('./models/my_model.gpt')
# note that we will now have "Init: OFF" in the progress bar

```
```bash
Training [168/tokens, 14M/params] - HurNet: [Init: OFF, Layer: OFF, Fit: OFF]: 5568it [00:30, 182.44it/s, loss=0.00297, precision=0.997]
```
```python
from hurmodel import HurModel
hurmodel = HurModel()
hurmodel.loadModel('./models/my_model.gpt')
hurmodel.print_predict(prompt='What is the main language spoken in Spain?', stream=True)

```
```bash
The main language spoken in Spain is Spanish.
```
When the "hurnet_layer" parameter is enabled, it inserts a layer of weights from the HurNet network into the Transformer network. This allows the training to abstract more subtle patterns that a conventional Transformer network would not be able to abstract.
```python
from hurmodel import HurModel
hurmodel = HurModel()
# the "hurnet_layer" parameter receives a boolean value, which when equal to True will insert a layer of neurons from the hurNet network into the current structure
# the default value of the "hurnet_layer" parameter is False, aiming for performance over learning subtle patterns
# we recommend using hurnet layers only when there are very subtle differences in the training data, where small differences can completely change the answer
# when the training data is considerably heterogeneous, it is worth keeping the parameter disabled to save processing
hurmodel.train('./dataset.json', hurnet_layer=True) # enables the merging of the hurnet architecture with the transformer architecture
hurmodel.saveModel('./models/my_model.gpt')
# note that we will now have "Layer: ON" in the progress bar

```
```bash
Training [168/tokens, 14M/params] - HurNet: [Init: ON, Layer: ON, Fit: OFF]: 5568it [00:34, 161.77it/s, loss=0.153, precision=0.847]
```
```python
from hurmodel import HurModel
hurmodel = HurModel()
hurmodel.loadModel('./models/my_model.gpt')
hurmodel.print_predict(prompt='How much is 2 + 2?', stream=True)

```
If the answer is incorrect, it is worth retraining the model with a lower accuracy threshold, as the HurNet layer is very sensitive to pattern abstraction and may abstract unnecessary patterns if the accuracy is too high.
```bash
The sum of 2 + 2 in mathematics is 4.
```
The "hurnet_fit" parameter can be used to enable assistance from the HurNet neural network in the weights adjustment process during training. In this case, a simplification of the complete HurNet network architecture will be used, aiming at dynamism between data exchange with the Transformer architecture.
```python
from hurmodel import HurModel
hurmodel = HurModel()
# the "hurnet_fit" parameter receives a boolean value, which when equal to True will enable training with the hurnet network, when equal to False the method maintains the conventional training of transformers (the default value is False)
# when "hurnet_fit" is enabled it starts the weight adjustment with the hurnet network, the adjustment can be complete or partial working together with the adjustment of the transformers
# adjustment with the hurnet network tends to be faster, but slightly less accurate depending on the dataset used in training
hurmodel.train('./dataset.json', hurnet_fit=True) # enables auxiliary adjustment of weights with the hurnet neural network
hurmodel.saveModel('./models/my_model.gpt')
# note that we will now have "Fit: ON" in the progress bar

```
Prefer to enable this feature when lower final accuracy is desired.
```bash
Training [168/tokens, 14M/params] - HurNet: [Init: ON, Layer: OFF, Fit: ON]: 5568it [00:34, 162.09it/s, loss=0.248, precision=0.752]
```
```python
from hurmodel import HurModel
hurmodel = HurModel()
hurmodel.loadModel('./models/my_model.gpt')
hurmodel.print_predict(prompt='Who discovered Brazil?', stream=True)

```
```bash
Brazil was discovered by Portuguese navigators led by Pedro Alvares Cabral in 1500.
```
Check out an example below with all the training method parameters in their respective orders and their respective default values.
```python
from hurmodel import HurModel
hurmodel = HurModel()
# the "dataset_path" and "string" parameters have an empty string as default value
hurmodel.train( # function for model training
    dataset_path='./dataset.json', # path to the training dataset in json or txt format
    string='', # string with optional complementary text for training
    precision=1, # approximate desired "precision/accuracy"
    tokenizer='gpt', # tokenizer for converting text into embeddings vectors
    context_window=None, # desired context window size
    hurnet_initializer=True, # intelligent initialization of weights with deterministic values
    hurnet_layer=False, # hurnet network layer insertion for subtle pattern abstraction
    hurnet_fit=False, # hybrid training with auxiliary adjustment of weights of the hurnet network
    end_tag=None, # subtext used as separator of input and output pairs in the file and/or training string
    progress=True # enables or disables the visualization of training progress
) # returns a dictionary with the training metrics
hurmodel.saveModel('./models/my_model.gpt')

```
```bash
Training [168/tokens, 14M/params] - HurNet: [Init: ON, Layer: OFF, Fit: OFF]: 5568it [00:29, 187.82it/s, loss=0.00909, precision=0.991]
```
```python
from hurmodel import HurModel
hurmodel = HurModel()
hurmodel.loadModel('./models/my_model.gpt') # always load the model before running the "predict" or "print_predict" function
hurmodel.print_predict( # displays the response to the input prompt
    prompt='Hello! Who are you?', # input for which you want to obtain an output
    max_tokens=500, # approximate maximum number of tokens in the response
    temperature=0.5, # inference temperature for the level of variability in responses
    stream=True # enables or disables real-time display on a token-by-token basis
)

```
```bash
Hello! I am Sapiens Chat, an AI model created by Sapiens Technology.
```
The model's training hyperparameters are configured automatically, but if you prefer, you can define them manually in the class constructor.
```python
from hurmodel import HurModel
# setting the values of the training hyperparameters in the class constructor causes the values to no longer be adjusted dynamically but instead be adjusted manually
# the default value for each of these parameters is None, when one or more parameters are set to None these parameters with None will be automatically set during training which will try to find the best value for the current situation
# you can leave them all as None so that they are all configured automatically, or you can manually configure one or more of them
# below is an example with all hyperparameters being configured manually
hurmodel = HurModel( # object class constructor
    embedding_dim=256, # amount of elements per token vector, each token will be converted into a vector with that amount of numbers
    block_size=64, # maximum number of tokens for the context window size
    batch_size=8, # maximum number of input-output pairs read at once during training
    number_heads=4, # number of attention mechanisms paying attention to different parts of the text at the same time
    number_layers=4, # number of hidden layers in the network, the higher this number, the greater the pattern abstraction
    dropout=0.2, # percentage (between 0 and 1) of neurons turned off at each step to prevent the model from memorizing the answers and actually learn instead of just memorizing
    learning_rate=0.0001, # learning speed, if too high the model learns little and quickly, if too low it learns a lot but slowly (preferably between 0 and 1)
    epochs=100 # number of times all data is read for learning, if too high the model runs the risk of starting to memorize instead of learning
)
hurmodel.train('./dataset.json')
hurmodel.saveModel('./models/my_model.gpt')

```
```bash
Training [168/tokens, 32M/params] - HurNet: [Init: ON, Layer: OFF, Fit: OFF]: 1890it [00:35, 52.74it/s, loss=0.0603, precision=0.94]
```
```python
from hurmodel import HurModel
hurmodel = HurModel()
hurmodel.loadModel('./models/my_model.gpt')
hurmodel.print_predict(prompt='Who discovered Brazil?', stream=True)

```
```bash
Brazil was discovered by Portuguese navigators led by Pedro Alvares Cabral in 1500.
```
The value of the "dropout" parameter can also be changed through the class's public variable right after the constructor is instantiated.
```python
from hurmodel import HurModel
hurmodel = HurModel()
hurmodel.dropout = 0.2
hurmodel.train('./dataset.json')
hurmodel.saveModel('./models/my_model.gpt')

```
```bash
Training [168/tokens, 14M/params] - HurNet: [Init: ON, Layer: OFF, Fit: OFF]: 5568it [00:30, 184.75it/s, loss=0.0391, precision=0.961]
```
It is also possible to view the total number of model parameters through the "parameters_number" variable. This variable with the number of parameters can be accessed through the class object right after training or loading the model.
```python
from hurmodel import HurModel
hurmodel = HurModel()
hurmodel.loadModel('./models/my_model.gpt')
parameters_number = hurmodel.parameters_number # get the total number of parameters of the trained model
print(f'The loaded model has {parameters_number} parameters in total.')
hurmodel.print_predict(prompt='Who discovered Brazil?', stream=True)

```
```bash
The loaded model has 14003253 parameters in total.                                                                                                              
Brazil was discovered by Portuguese navigators led by Pedro Alvares Cabral in 1500.
```
The "addFit" method when called before the "train" method, as well as the "string" parameter, can also be used to complement the training dataset.
```python
from hurmodel import HurModel
hurmodel = HurModel()
# the "addFit" method is being used to complement the training data
# note: when called before training, it is not a fine-tuning because it is part of the original data
hurmodel.addFit('What does the acronym GPT mean in language models?', 'GPT in language models stands for Generative Pre-trained Transformer.')
hurmodel.addFit('What is the capital of Spain?', 'The capital of Spain is Madrid.')
hurmodel.train('./dataset.json')
hurmodel.saveModel('./models/my_model.gpt')

```
```bash
Training [168/tokens, 14M/params] - HurNet: [Init: ON, Layer: OFF, Fit: OFF]: 5568it [00:29, 187.16it/s, loss=0.00624, precision=0.994]
```
This technique makes inference from the added data more error-prone than fine-tuning which is more reliable.
```python
from hurmodel import HurModel
hurmodel = HurModel()
hurmodel.loadModel('./models/my_model.gpt')
hurmodel.print_predict('Hello! Who are you?', stream=True)

```
```bash
Hello! I am Sapiens Chat, an AI model created by Sapiens Technology.
```
The "addFit" method when invoked after a model training or loading, can be used to add fits to the trained or loaded model.
```python
from hurmodel import HurModel
hurmodel = HurModel()
hurmodel.train('./dataset.json')
# you can fine-tune a model right after training by calling the "addFit" method which will readjust the weights based on the new input-output pairs added
hurmodel.addFit('What does the acronym GPT mean in language models?', 'GPT in language models stands for Generative Pre-trained Transformer.')
hurmodel.addFit('What is the capital of Spain?', 'The capital of Spain is Madrid.')
# save the model with the training data adjusted with the two input and output pairs added above
# you can add as many pairs as you want to your fit
hurmodel.saveModel('./models/my_model.gpt')

```
```bash
Training [168/tokens, 14M/params] - HurNet: [Init: ON, Layer: OFF, Fit: OFF]: 5568it [00:29, 187.16it/s, loss=0.00624, precision=0.994]
```
It is also possible to view the total number of model parameters through the "parameters_number" variable. This variable with the number of parameters can be accessed through the class object right after training or loading the model.
```python
from hurmodel import HurModel
hurmodel = HurModel()
hurmodel.loadModel('./models/my_model.gpt')

hurmodel.print_predict(prompt='Hello! Who are you?', stream=True)
hurmodel.print_predict(prompt='What does the acronym GPT mean in language models?', stream=True)
hurmodel.print_predict(prompt='What is the capital of Spain?', stream=True)

```
```bash
Hello! I am Sapiens Chat, an AI model created by Sapiens Technology.                                                                                            
GPT in language models stands for Generative Pre-trained Transformer.
The capital of Spain is Madrid.
```
Fine-tuning with the "addFit" method can also be done on a pre-trained model after loading.
```python
from hurmodel import HurModel
hurmodel = HurModel()
hurmodel.train('./dataset.json')
save_model = hurmodel.saveModel('./models/my_model.gpt') # returns True if the model is saved successfully, or False otherwise
if save_model: print(f'Model saved with {hurmodel.parameters_number} parameters.') # displays a save confirmation message
else: print('ERROR saving the model!!') # if an error occurs while saving, an error message is displayed.

```
```bash
Training [168/tokens, 14M/params] - HurNet: [Init: ON, Layer: OFF, Fit: OFF]: 5568it [00:30, 184.92it/s, loss=0.113, precision=0.887]                           
Model saved with 14003253 parameters.
```
```python
from hurmodel import HurModel
hurmodel = HurModel()
# load the model
hurmodel.loadModel('./models/my_model.gpt')
# applies fine-tuning to the model
hurmodel.addFit('What does the acronym GPT mean in language models?', 'GPT in language models stands for Generative Pre-trained Transformer.')
hurmodel.addFit('What is the capital of Spain?', 'The capital of Spain is Madrid.')
# saves a new model with the fine-tuning applied
if hurmodel.saveModel('./models/adjusted_model.gpt'): print('Adjusted model saved successfully.')
else: print('Error applying fine tuning!!')

```
```bash
Adjusted model saved successfully.
```
```python
from hurmodel import HurModel
hurmodel = HurModel()
hurmodel.loadModel('./models/adjusted_model.gpt') # loading of the adjusted model

hurmodel.print_predict(prompt='Hello! Who are you?', stream=True)
hurmodel.print_predict(prompt='What does the acronym GPT mean in language models?', stream=True)
hurmodel.print_predict(prompt='What is the capital of Spain?', stream=True)

```
```bash
Hello! I am Sapiens Chat, an AI model created by Sapiens Technology.                                                                                            
GPT in language models stands for Generative Pre-trained Transformer.
The capital of Spain is Madrid.
```
You can define a minimum percentage (between 0 and 1) using the "precision" parameter, so that the fine-tuning responses will only be returned when the user prompt reaches this level of similarity with the tuning input.
```python
from hurmodel import HurModel
hurmodel = HurModel()
# load the model
hurmodel.loadModel('./models/my_model.gpt')
# applies fine-tuning to the model
# preferably use the same minimum precision for all pairs, otherwise the final precision considered will be an average of all precisions
hurmodel.addFit('What does the acronym GPT mean in language models?', 'GPT in language models stands for Generative Pre-trained Transformer.', precision=0.7) # this response will only be returned when the prompt has at least 70% similarity to the adjustment input
hurmodel.addFit('What is the capital of Spain?', 'The capital of Spain is Madrid.', precision=0.7) # this response will only be returned when the prompt has at least 70% similarity to the adjustment input
# saves a new model with the fine-tuning applied
if hurmodel.saveModel('./models/adjusted_model.gpt'): print('Adjusted model saved successfully.')
else: print('Error applying fine tuning!!')

```
```bash
Adjusted model saved successfully.
```
```python
from hurmodel import HurModel
hurmodel = HurModel()
hurmodel.loadModel('./models/adjusted_model.gpt') # loading of the adjusted model

hurmodel.print_predict(prompt='Hello! Who are you?', stream=True)
hurmodel.print_predict(prompt='What does the acronym GPT mean in language models?', stream=True)
hurmodel.print_predict(prompt='What is the capital of Spain?', stream=True)

```
```bash
Hello! I am Sapiens Chat, an AI model created by Sapiens Technology.                                                                                            
GPT in language models stands for Generative Pre-trained Transformer.
The capital of Spain is Madrid.
```
To obtain the result of the training metrics, simply capture the return of the "train" function.
```python
# we are setting the following values in the below class: (embedding_dim: 256; block_size: 64; batch_size: 8; number_heads: 4; number_layers: 4; dropout: 0.2; learning_rate: 0.0001; epochs: 100)
hurmodel = HurModel(256, 64, 8, 4, 4, 0.2, 0.0001, 100)
training_metrics = hurmodel.train('./dataset.json') # obtains a dictionary in the following format: {'val_loss': 0.0, 'loss': 0.0, 'generalization_rate': 0.0, 'precision': 0.0}
val_loss = training_metrics['val_loss'] # value of information loss during validation of test data (test data is separate and not part of training)
loss = training_metrics['loss'] # final loss of information, during the computation of the raw training data
generalization_rate = training_metrics['generalization_rate'] # rate referring to how well the model is able to generalize, that is, how much the model can adapt to inputs different from the inputs used in training
precision = training_metrics['precision'] # final accuracy of the model that corresponds to the confidence rate in the responses for the future inferences (reliability of inferences)
# displays training metrics (display with eight decimal places)
print(f'Loss in validation test: {val_loss:.8f}')
print(f'Loss in training: {loss:.8f}')
print(f'Generalization ability: {generalization_rate:.8f}')
print(f'Model reliability: {precision:.8f}')
hurmodel.saveModel('./models/my_model.gpt')

```
```bash
Training [168/tokens, 32M/params] - HurNet: [Init: ON, Layer: OFF, Fit: OFF]: 1890it [00:36, 52.17it/s, loss=0.0486, precision=0.951]                           
Loss in validation test: 0.02931614
Loss in training: 0.04856423
Generalization ability: 0.97068386
Model reliability: 0.95143577
```
```python
from hurmodel import HurModel
hurmodel = HurModel()
hurmodel.loadModel('./models/my_model.gpt')
hurmodel.print_predict(prompt='Who discovered Brazil?', stream=True)

```
```bash
Brazil was discovered by Portuguese navigators led by Pedro Alvares Cabral in 1500.
```

## Methods
### Construtor: HurModel
Parameters (If not assigned, they will be configured automatically)
| Name                | Description                                                                                                                                                                                              | Type  | Default Value    |
|---------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------|------------------|
| embedding_dim       | amount of elements per token vector, each token will be converted into a vector with that amount of numbers                                                                                              | int   | None             |
| block_size          | maximum number of tokens for the context window size                                                                                                                                                     | int   | None             |
| batch_size          | maximum number of input-output pairs read at once during training                                                                                                                                        | int   | None             |
| number_heads        | number of attention mechanisms paying attention to different parts of the text at the same time                                                                                                          | int   | None             |
| number_layers       | number of hidden layers in the network, the higher this number, the greater the pattern abstraction                                                                                                      | int   | None             |
| dropout             | percentage (between 0 and 1) of neurons turned off at each step to prevent the model from memorizing the answers and actually learn instead of just memorizing                                           | float | None             |
| learning_rate       | learning speed, if too high the model learns little and quickly, if too low it learns a lot but slowly (preferably between 0 and 1)                                                                      | float | None             |
| epochs              | number of times all data is read for learning, if too high the model runs the risk of starting to memorize instead of learning                                                                           | int   | None             |

### train (function return type: dict): Returns a dictionary with the training metrics.
Parameters
| Name                | Description                                                                                                                                                                                              | Type  | Default Value     |
|---------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------|-------------------|
| dataset_path        | path to a local or web dataset in txt or preferably json format                                                                                                                                          | str   | ''                |
| string              | text to train the model, or to complement the dataset                                                                                                                                                    | str   | ''                |
| precision           | percentage accuracy or reliability between 0 and 1 desired during weights adjustment, which when achieved will end the training                                                                          | float | 1.0               |
| tokenizer           | type of encoder used in converting text into sequence of embeddings (gpt to encode chunks of words, or sapi to encode each character individually)                                                       | str   | 'gpt'             |
| context_window      | maximum number of tokens accepted in the inference prompt                                                                                                                                                | int   | None              |
| hurnet_initializer  | if True enables smart initialization of weights with the hurnet network, if False uses default initialization with random weights                                                                        | bool  | True              |
| hurnet_layer        | if True adds layer with the hurnet network architecture, if False it remains only with the transformer network traditional layers                                                                        | bool  | False             |
| hurnet_fit          | if True, will receive assistance from the hurnet network for adjusting weights, if False, it will only apply traditional backpropagation in the adjustments                                              | bool  | False             |
| end_tag             | defines what subtext in the training data will be used to separate input and output pairs from each other                                                                                                | str   | None              |
| progress            | if True enables visualization of training progress, if False disables visualization of training progress                                                                                                 | bool  | True              |

### saveModel (function return type: bool): Returns True if the model is saved successfully, or False otherwise.
Parameters
| Name                | Description                                                                                                                                                                                              | Type  | Default Value     |
|---------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------|-------------------|
| model_path          | local path with directory and name for the trained model generation                                                                                                                                      | str   | ''                |
| progress            | if True enables the progress bar that displays the current stage of saving, if False will hide the progress bar                                                                                          | bool  | True              |

### loadModel (function return type: bool): Returns True if the model is loaded successfully, or False otherwise.
Parameters
| Name                | Description                                                                                                                                                                                              | Type  | Default Value     |
|---------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------|-------------------|
| model_path          | local path with the directory and file name of the model that will be loaded                                                                                                                             | str   | ''                |
| progress            | if True enables the progress bar that displays the current stage of loading, if False will hide the progress bar                                                                                         | bool  | True              |

### addFit (function return type: bool): Returns True if an of "input/prompt/instruction/question" and "output/answer" pair is successfully added to the current model, or False otherwise.
Parameters
| Name                | Description                                                                                                                                                                                              | Type  | Default Value     |
|---------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------|-------------------|
| prompt              | input for which you want to obtain an output                                                                                                                                                             | str   | ''                |
| answer              | desired output for when a similar input is made to the inference                                                                                                                                         | str   | ''                |
| precision           | minimum percentage (between 0 and 1) of similarity required between the added input and the inference prompt, so that the added output is returned as the answer                                         | float | 0.5               |

### predict (function return type: str/generator object): Returns a string with the response to the user prompt.
Parameters
| Name                | Description                                                                                                                                                                                              | Type  | Default Value     |
|---------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------|-------------------|
| prompt              | input for which you want to infer a response                                                                                                                                                             | str   | ''                |
| max_tokens          | approximate maximum number of tokens in the response text                                                                                                                                                | int   | 500               |
| temperature         | percentage (between 0 and 1) for how different one answer will be from another when the same input/question is asked (the answers will remain the same when the training dataset is small)               | float | 0.5               |
| stream              | if True, returns a token generator to obtain one token at a time with the response being generated in real time, if False, will return the complete response  only when all tokens are generated         | bool  | False             |

### print_predict (method without return): Displays a string with the model prediction/inference result.
Parameters
| Name                | Description                                                                                                                                                                                              | Type  | Default Value     |
|---------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------|-------------------|
| prompt              | input for which you want to display a response                                                                                                                                                           | str   | ''                |
| max_tokens          | approximate maximum number of tokens in the response text                                                                                                                                                | int   | 500               |
| temperature         | percentage (between 0 and 1) for how different one answer will be from another when the same input/question is asked (the answers will remain the same when the training dataset is small)               | float | 0.5               |
| stream              | if True, will display the response in real time with one token at a time, if False, will display the complete response only when all tokens are generated                                                | bool  | False             |

Check out now a comparison between a conventional Transformer architecture model and our semantic comparison architecture with HurNet.
```bash
pip install torch tiktoken
```
```python
# this is a code of a transformer algorithm for gpt models; it belongs to sapiens technology® and its unauthorized use by third parties is strictly prohibited
# !pip install torch tiktoken or !pip install torch==2.4.1 and then !pip install tiktoken==0.4.0
class GPTModel: # main class for a standard pre-trained generative transformer model
    def __init__(self): # gpt model architecture builder
        from torch.utils.data import Dataset, DataLoader
        from torch import nn, triu, ones
        from torch.nn import Module, functional as F, utils
        from torch import no_grad, tensor, int64, multinomial, cat, save, load
        from json import load as json_load
        from tiktoken import get_encoding
        from torch import optim
        from tqdm import tqdm
        from os import path as os_path, makedirs as os_makedirs
        from torch import cuda, device, backends        
        if cuda.is_available(): local_device = device('cuda')
        elif backends.mps.is_available(): local_device = device('mps')
        else: local_device = device('cpu')
        self.__Dataset = Dataset
        self.__Module = Module
        self.__nn = nn
        self.__tensor = tensor
        self.__triu = triu
        self.__ones = ones
        self.__no_grad = no_grad
        self.__device = local_device
        self.__F = F
        self.__int64 = int64
        self.__multinomial = multinomial
        self.__cat = cat
        self.__json_load = json_load
        self.__get_encoding = get_encoding
        self.__DataLoader = DataLoader
        self.__optim = optim
        self.__utils = utils
        self.__tqdm = tqdm
        self.__os_path = os_path
        self.__os_makedirs = os_makedirs
        self.__save = save
        self.__load = load
        self.__model = None
        self.__encode = None
        self.__block_size = 500
        self.__decode = None
        self.__string = ''
        self.__vocab_size = 0
        self.__char_to_idx = {}
        self.__idx_to_char = {}
        self.__tokenizer = 'sapi'
        self.__batch_size = 32
        self.__embedding_dim = 384
        self.__number_heads = 6
        self.__number_layers = 6
        self.__dropout = 0.1
        self.__optimizer = None
        self.__learning_rate = 3e-4
        self.__eval_interval = 500
        self.__train = False
        self.parameters_number = 0
        class TextDataset(self.__Dataset): # class for processing training data
            def __init__(self, data={}, block_size=0): self.data, self.block_size = data, block_size
            def __len__(self): return len(self.data) - self.block_size
            def __getitem__(self, index=0):
                input_sequence = self.data[index:index + self.block_size]
                target_sequence = self.data[index + 1:index + self.block_size + 1]
                return input_sequence, target_sequence
        self.__TextDataset = TextDataset
        class Transformer(self.__Module): # building transformer architecture
            def __init__(self, outer=None, vocab_size=0, embedding_dim=0, number_heads=0, number_layers=0, dropout=None, block_size=0):
                super().__init__()
                self.outer = outer
                self.embedding = outer._GPTModel__nn.Embedding(vocab_size, embedding_dim)
                self.pos_encoder = outer._GPTModel__nn.Parameter(outer._GPTModel__tensor([]).new_zeros(1, block_size, embedding_dim))
                self.transformer = outer._GPTModel__nn.TransformerDecoder(outer._GPTModel__nn.TransformerDecoderLayer(d_model=embedding_dim, nhead=number_heads, dropout=dropout), num_layers=number_layers)
                self.fc_out = outer._GPTModel__nn.Linear(embedding_dim, vocab_size)
                self.dropout = outer._GPTModel__nn.Dropout(dropout)
                self.block_size = block_size
            def forward(self, input_tensor=[]):
                outer = self.outer
                batch_size, seq_len = input_tensor.size()
                positions = self.pos_encoder[:, :seq_len, :].to(input_tensor.device)
                embedded = self.dropout(self.embedding(input_tensor) + positions)
                transposed = embedded.transpose(0, 1)
                mask = outer._GPTModel__triu(outer._GPTModel__ones(seq_len, seq_len, device=input_tensor.device) * float('-inf'), diagonal=1)
                output = self.transformer(transposed, transposed, tgt_mask=mask)
                output = output.transpose(0, 1)
                return self.fc_out(output)
        self.__Transformer = Transformer
    def __compute_loss(self, loader=[]): # function for computing network loss rate
        self.__model.eval()
        total_loss = 0
        with self.__no_grad():
            for input_batch, target_batch in loader:
                input_batch, target_batch = input_batch.to(self.__device), target_batch.to(self.__device)
                logits = self.__model(input_batch)
                loss = self.__F.cross_entropy(logits.view(-1, logits.size(-1)), target_batch.view(-1))
                total_loss += loss.item()
        return total_loss / len(loader)
    def __format_params(self, number_params=0): # function for formatting the number of network parameters
        if number_params < 1_000_000: return f'{number_params}P'
        elif number_params < 1_000_000_000: return f'{number_params // 1_000_000}M'
        elif number_params < 1_000_000_000_000: return f'{number_params // 1_000_000_000}B'
        else: return f'{number_params // 1_000_000_000_000}T'
    def __generate_tokens(self, prompt='', max_tokens=500, temperature=1.0): # function to generate the predicted tokens in the inference
        self.__model.eval()
        encoded_prompt = self.__encode(prompt)
        input_tensor = self.__tensor(encoded_prompt, dtype=self.__int64).unsqueeze(0).to(self.__device)
        with self.__no_grad():
            tokens_generated = 0
            while True:
                conditioned_input = input_tensor[:, -self.__block_size:] if input_tensor.size(1) > self.__block_size else input_tensor
                logits = self.__model(conditioned_input)
                logits = logits[:, -1, :] / temperature
                probs = self.__F.softmax(logits, dim=-1)
                next_token = self.__multinomial(probs, num_samples=1)
                input_tensor = self.__cat((input_tensor, next_token), dim=1)
                token = next_token.item()
                decoded_token = self.__decode([token])
                if tokens_generated == 0 and '\n' in decoded_token: continue
                tokens_generated += 1
                yield decoded_token
                if (tokens_generated >= max_tokens and decoded_token[-1] in {'.', '\n', '!', '?', ';'}) or (tokens_generated >= (max_tokens*2)): break
    def train(self, dataset_path='', tokenizer='sapi', precision=0.5, context_window=500, progress=True): # function for training a conventional transformer model
        try:
            """
                Arguments:
                    dataset_path: receives a string with the address of a txt or json file for model training  
                    tokenizer: receives a string with the value 'sapi' to use sapiens' tokenizer, or 'gpt' to use the generative pre-trained transformer tokenizer  
                    precision: receives a float with a target value for the precision of weights adjustment in backpropagation; backpropagation will only stop if this target is reached  
                    context_window: receives an integer with the limit for the context window to be created for the model  
                    progress: receives a boolean indicating whether the progress bar will be displayed or hidden  
            """
            dataset_path = str(dataset_path).strip()
            tokenizer = str(tokenizer).lower().strip()
            precision = float(precision) if type(precision) in (bool, int, float) else 0.5
            context_window = max((1, int(context_window))) if type(context_window) in (bool, int, float) else 500
            progress = bool(progress) if type(progress) in (bool, int, float) else True
            self.__block_size = context_window
            loss_limit = max(0, min(1, 1 - precision))
            is_txt, is_json, formatted_sequences = dataset_path.endswith('.txt'), dataset_path.endswith('.json'), []
            if not is_txt and not is_json: raise ValueError('Unsupported file format. Use .txt or .json')
            if is_txt:
                with open(dataset_path, 'r', encoding='utf-8') as file: text_data = file.read()
            elif is_json:
                with open(dataset_path, 'r', encoding='utf-8') as file: json_data = self.__json_load(file)
                if type(json_data) == dict:
                    data_key = list(json_data.keys())[0]
                    pairs = json_data[data_key]
                else: pairs = json_data
                formatted_sequences = [str(pair[list(pair.keys())[0]]+'\n'+pair[list(pair.keys())[1]]).strip() for pair in pairs]
                text_data = '\n\n'.join(formatted_sequences)
            if len(self.__string) > 0: text_data += '\n\n'+self.__string
            text_data = text_data.strip()
            if tokenizer == 'sapi':
                chars = sorted(list(set(text_data)))
                self.__vocab_size = len(chars)
                self.__char_to_idx = {char: index for index, char in enumerate(chars)}
                self.__idx_to_char = {index: char for index, char in enumerate(chars)}
                self.__encode = lambda string: [self.__char_to_idx[char] for char in string]
                self.__decode = lambda indices: ''.join([self.__idx_to_char[index] for index in indices])
            else:
                encode = self.__get_encoding('gpt2')
                self.__vocab_size = encode.n_vocab
                self.__encode = encode.encode
                self.__decode = encode.decode
            data = self.__tensor(self.__encode(text_data), dtype=self.__int64)
            split_point = int(0.9 * len(data))
            train_data = data[:split_point]
            val_data = data[split_point:]
            if len(train_data) < self.__block_size:
                if len(train_data) > 1: self.__block_size = len(train_data) - 1
                else: raise ValueError('Dataset too small for training. Add more data.')
            self.__tokenizer = tokenizer
            train_dataset = self.__TextDataset(train_data, self.__block_size)
            val_dataset = self.__TextDataset(val_data, self.__block_size)
            train_loader = self.__DataLoader(train_dataset, batch_size=self.__batch_size, shuffle=True)
            val_loader = self.__DataLoader(val_dataset, batch_size=self.__batch_size, shuffle=False)
            self.__model = self.__Transformer(self, self.__vocab_size, self.__embedding_dim, self.__number_heads, self.__number_layers, self.__dropout, self.__block_size).to(self.__device)
            self.__optimizer = self.__optim.AdamW(self.__model.parameters(), lr=self.__learning_rate)
            scheduler = self.__optim.lr_scheduler.ReduceLROnPlateau(self.__optimizer, mode='min', factor=0.5, patience=3)
            epoch, step, best_val_loss = 0, 0, float('inf')            
            while True:
                self.__model.train()
                total_train_loss = 0
                str_epoch = str(epoch+1).rjust(10, '0')
                for input_batch, target_batch in train_loader:
                    input_batch, target_batch = input_batch.to(self.__device), target_batch.to(self.__device)
                    logits = self.__model(input_batch)
                    loss = self.__F.cross_entropy(logits.view(-1, logits.size(-1)), target_batch.view(-1))
                    self.__optimizer.zero_grad()
                    loss.backward()
                    self.__utils.clip_grad_norm_(self.__model.parameters(), 1.0)
                    self.__optimizer.step()
                    total_train_loss += loss.item()
                    if step > 0 and step % self.__eval_interval == 0:
                        val_loss = self.__compute_loss(val_loader)
                        scheduler.step(val_loss)
                        if val_loss < best_val_loss: best_val_loss = val_loss
                    step += 1
                avg_train_loss = total_train_loss / len(train_loader)
                if avg_train_loss <= loss_limit:
                    if progress: print()
                    break
                elif progress:
                    format_str = '{desc}: {percentage:3.0f}%|{bar:10}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]'
                    current_precision = max(0, min(1, 1 - avg_train_loss))
                    str_current_precision = f'{current_precision:.4f}'.ljust(5, '0')
                    str_precision = f'{precision:.4f}'.ljust(5, '0')
                    train_loader = self.__tqdm(train_loader, desc=f'Epoch {str_epoch} - current precision is {str_current_precision}; aiming for precision >= {str_precision} in training', bar_format=format_str)
                epoch += 1
            return True
        except Exception as error:
            print('ERROR in train: ' + str(error))
            return False
    def saveModel(self, model_path='', progress=True): # function to save a pre-trained model
        try:
            """
                Arguments:
                    model_path: receives a string with the address and name of the model file to be generated  
                    progress: receives a boolean indicating whether the progress bar will be displayed or hidden  
            """
            model_path = str(model_path).strip()
            progress = bool(progress) if type(progress) in (bool, int, float) else True
            if self.__model is None: raise ValueError('Model is not initialized. Call train or loadModel first.')
            number_params = sum(p.numel() for p in self.__model.parameters())
            formatted_params = self.__format_params(number_params)
            if isinstance(model_path, str):
                directory, file_name = self.__os_path.split(model_path)
                if not file_name: file_name = 'model.gpt'
                elif not file_name.endswith('.gpt'): file_name += '.gpt'
            else: directory, file_name = str(model_path), 'model.gpt'
            if directory and not self.__os_path.exists(directory): self.__os_makedirs(directory)
            save_path = self.__os_path.join(directory, file_name)
            save_dict = {'model_state_dict': self.__model.state_dict(), 'tokenizer': self.__tokenizer, 'vocab_size': self.__vocab_size, 'block_size': self.__block_size}
            if self.__tokenizer == 'sapi': save_dict['char_to_idx'], save_dict['idx_to_char'] = self.__char_to_idx, self.__idx_to_char
            if progress:
                for _ in self.__tqdm(range(10), desc=f'Saving model with {formatted_params} parameters', leave=False): self.__save(save_dict, save_path)
            else: self.__save(save_dict, save_path)
            self.__train = True
            return True
        except Exception as error:
            print('ERROR in saveModel: ' + str(error))
            return False
    def loadModel(self, model_path='', progress=True): # function to load a previously saved pre-trained model
        try:
            """
                Arguments:
                    model_path: receives a string with the address and name of the model file to be loaded  
                    progress: receives a boolean indicating whether the progress bar will be displayed or hidden  
            """
            model_path = str(model_path).strip()
            progress = bool(progress) if type(progress) in (bool, int, float) else True
            if len(model_path) > 0:
                directory, file_name = self.__os_path.split(model_path)
                if not file_name: file_name = 'model.gpt'
                elif not file_name.endswith('.gpt'): file_name += '.gpt'
            else: directory, file_name = str(model_path), 'model.gpt'
            model_file = self.__os_path.join(directory, file_name)
            if progress:
                for _ in self.__tqdm(range(10), desc='Loading model', leave=False): checkpoint = self.__load(model_file, map_location=self.__device)
            else: checkpoint = self.__load(model_file, map_location=self.__device)
            self.__tokenizer = checkpoint['tokenizer']
            self.__vocab_size = checkpoint['vocab_size']
            self.__block_size = checkpoint['block_size']
            if self.__tokenizer == 'sapi':
                self.__char_to_idx = checkpoint['char_to_idx']
                self.__idx_to_char = checkpoint['idx_to_char']
                self.__encode = lambda string: [self.__char_to_idx[char] for char in string]
                self.__decode = lambda indices: ''.join([self.__idx_to_char[index] for index in indices])
            else:
                encode = self.__get_encoding('gpt2')
                self.__encode = encode.encode
                self.__decode = encode.decode
            self.__model = self.__Transformer(self, self.__vocab_size, self.__embedding_dim, self.__number_heads, self.__number_layers, self.__dropout, self.__block_size).to(self.__device)
            self.__model.load_state_dict(checkpoint['model_state_dict'])
            number_params = sum(p.numel() for p in self.__model.parameters())
            self.parameters_number, self.__optimizer, self.__train = number_params, None, True
            return True
        except Exception as error:
            print('ERROR in loadModel: ' + str(error))
            return False
    def addFit(self, prompt='', answer=''): # function to add fine-tuning to a dataset before training, or to a previously loaded model
        try:
            """
                Arguments:
                    prompt: receives a string with the input sample to be added to the current model  
                    answer: receives a string with the output sample to be added to the current model  
            """
            prompt = str(prompt).strip()
            answer = str(answer).strip()
            if not self.__train: self.__string += prompt+'\n'+answer+'\n\n'
            else:
                if self.__model is None: raise ValueError('Model is not initialized. Call train or loadModel first.')
                if self.__optimizer is None: self.__optimizer = self.__optim.AdamW(self.__model.parameters(), lr=self.__learning_rate)
                formatted = prompt+'\n'+answer+'\n\n'
                encoded = self.__encode(formatted)
                if len(encoded) > self.__block_size: encoded = encoded[:self.__block_size]
                input_tensor = self.__tensor(encoded[:-1], dtype=self.__int64).unsqueeze(0).to(self.__device)
                target_tensor = self.__tensor(encoded[1:], dtype=self.__int64).unsqueeze(0).to(self.__device)
                self.__model.train()
                logits = self.__model(input_tensor)
                loss = self.__F.cross_entropy(logits.view(-1, logits.size(-1)), target_tensor.view(-1))
                self.__optimizer.zero_grad()
                loss.backward()
                self.__utils.clip_grad_norm_(self.__model.parameters(), 1.0)
                self.__optimizer.step()
            return True
        except Exception as error:
            print('ERROR in addFit: ' + str(error))
            return False
    def predict(self, prompt='', max_tokens=500, stream=False): # function to return the inference result
        try:
            """
                Arguments:
                    prompt: receives a string with the input for which an output is desired  
                    max_tokens: receives an integer with an approximate number for the maximum tokens to be generated in the response  
                    stream: receives a boolean indicating whether the response will be returned token by token or all at once  
            """
            prompt = str(prompt).strip()
            max_tokens = max((1, int(max_tokens))) if type(max_tokens) in (bool, int, float) else 500
            stream = bool(stream) if type(stream) in (bool, int, float) else False
            if self.__model is None: raise ValueError('Model is not initialized. Call train or loadModel first.')
            if stream: return self.__generate_tokens(prompt, max_tokens)
            tokens = list(self.__generate_tokens(prompt, max_tokens))
            return ''.join(tokens)
        except Exception as error:
            print('ERROR in predict: ' + str(error))
            return ''
    def print_predict(self, prompt='', max_tokens=500, stream=False): # method to display the inference result
        try:
            """
                Arguments:
                    prompt: receives a string with the input for which an output is desired  
                    max_tokens: receives an integer with an approximate number for the maximum tokens to be generated in the response  
                    stream: receives a boolean indicating whether the response will be displayed token by token or all at once  
            """
            prompt = str(prompt).strip()
            max_tokens = max((1, int(max_tokens))) if type(max_tokens) in (bool, int, float) else 500
            stream = bool(stream) if type(stream) in (bool, int, float) else False
            if self.__model is None: raise ValueError('Model is not initialized. Call train or loadModel first.')
            if stream:
            	[print(token, end='', flush=True) for token in self.__generate_tokens(prompt, max_tokens)]
            	print()
            else: print(self.predict(prompt, stream=False))
        except Exception as error:
            print('ERROR in print_predict: ' + str(error))
# this is a code of a transformer algorithm for gpt models; it belongs to sapiens technology® and its unauthorized use by third parties is strictly prohibited

```
```python
# ---> insert here the code of the GPTModel class defined above...
from time import time # import time module
start = time() # marks the initial time

gptmodel = GPTModel() # instantiation of the transformer class for the gpt model
# training the model with a text-based dataset using the gpt tokenizer and achieving 97% accuracy with a context window of 200 tokens
gptmodel.train(dataset_path='./dataset.txt', tokenizer='gpt', precision=0.97, context_window=200, progress=True)
gptmodel.saveModel(model_path='./gpt_model.gpt', progress=True) # saving the pre-trained generative model

# time measured using model save delay
end = time() # marks the end time
time_spent_gptmodel = abs(start-end) # calculates the time difference between the start and end of execution
print(f'\nRuntime: {time_spent_gptmodel} seconds.') # displays the total time spent in seconds

```
Runned on a Macbook M3 Max with 48GB of VRAM.
```bash
Epoch 0000000001 - current precision is 0.0000; aiming for precision >= 0.9700 in training: 100%|██████████| 9/9 [00:02<00:00,  3.04it/s]
Epoch 0000000002 - current precision is 0.0000; aiming for precision >= 0.9700 in training: 100%|██████████| 9/9 [00:02<00:00,  3.14it/s]
Epoch 0000000003 - current precision is 0.0000; aiming for precision >= 0.9700 in training: 100%|██████████| 9/9 [00:02<00:00,  3.11it/s]
Epoch 0000000004 - current precision is 0.0000; aiming for precision >= 0.9700 in training: 100%|██████████| 9/9 [00:02<00:00,  3.14it/s]
Epoch 0000000005 - current precision is 0.0000; aiming for precision >= 0.9700 in training: 100%|██████████| 9/9 [00:02<00:00,  3.15it/s]
Epoch 0000000006 - current precision is 0.3046; aiming for precision >= 0.9700 in training: 100%|██████████| 9/9 [00:02<00:00,  3.14it/s]
Epoch 0000000007 - current precision is 0.5124; aiming for precision >= 0.9700 in training: 100%|██████████| 9/9 [00:02<00:00,  3.13it/s]
Epoch 0000000008 - current precision is 0.6447; aiming for precision >= 0.9700 in training: 100%|██████████| 9/9 [00:02<00:00,  3.09it/s]
Epoch 0000000009 - current precision is 0.7412; aiming for precision >= 0.9700 in training: 100%|██████████| 9/9 [00:02<00:00,  3.12it/s]
Epoch 0000000010 - current precision is 0.8110; aiming for precision >= 0.9700 in training: 100%|██████████| 9/9 [00:02<00:00,  3.12it/s]
Epoch 0000000011 - current precision is 0.8303; aiming for precision >= 0.9700 in training: 100%|██████████| 9/9 [00:02<00:00,  3.13it/s]
Epoch 0000000012 - current precision is 0.8678; aiming for precision >= 0.9700 in training: 100%|██████████| 9/9 [00:02<00:00,  3.09it/s]
Epoch 0000000013 - current precision is 0.8966; aiming for precision >= 0.9700 in training: 100%|██████████| 9/9 [00:02<00:00,  3.13it/s]
Epoch 0000000014 - current precision is 0.9181; aiming for precision >= 0.9700 in training: 100%|██████████| 9/9 [00:02<00:00,  3.09it/s]
Epoch 0000000015 - current precision is 0.9268; aiming for precision >= 0.9700 in training: 100%|██████████| 9/9 [00:02<00:00,  3.13it/s]
Epoch 0000000016 - current precision is 0.9421; aiming for precision >= 0.9700 in training: 100%|██████████| 9/9 [00:02<00:00,  3.11it/s]
Epoch 0000000017 - current precision is 0.9543; aiming for precision >= 0.9700 in training: 100%|██████████| 9/9 [00:02<00:00,  3.12it/s]
Epoch 0000000018 - current precision is 0.9626; aiming for precision >= 0.9700 in training: 100%|██████████| 9/9 [00:02<00:00,  3.08it/s]
Epoch 0000000019 - current precision is 0.9682; aiming for precision >= 0.9700 in training: 100%|██████████| 9/9 [00:02<00:00,  3.08it/s]

                                                                                                                                                                
Runtime: 62.19831705093384 seconds.
```
```python
from time import time # import time module
start = time() # marks the initial time

from hurmodel import HurModel
hurmodel = HurModel() # instantiation of the transformer class for the hur model
# training the model with a text-based dataset using the gpt tokenizer and achieving 97% accuracy with a context window of 200 tokens
hurmodel.train(dataset_path='dataset.txt', tokenizer='gpt', precision=0.97, context_window=200, progress=True)
hurmodel.saveModel(model_path='./hur_model.gpt') # saving the pre-trained generative model

# time measured using model save delay
end = time() # marks the end time
time_spent_hurmodel = abs(start-end) # calculates the time difference between the start and end of execution
print(f'\nRuntime: {time_spent_hurmodel} seconds.') # displays the total time spent in seconds

```
Runned on a Macbook M3 Max with 48GB of VRAM.
The **HurModel** network was **3 times** faster in training than a conventional Transformer network using the same dataset.
```bash
Training [539/tokens, 16M/params] - HurNet: [Init: ON, Layer: OFF, Fit: OFF]: 4026it [00:18, 220.60it/s, loss=0.019, precision=0.981]                           
                                                                                                                                                                
Runtime: 20.04410696029663 seconds.
```
Now see an inference test with the generated models.
```python
# ---> insert here the code of the GPTModel class defined above...
# time measured using model loading delay
from time import time # import time module
start = time() # marks the initial time

gptmodel = GPTModel() # instantiation of the transformer class for the gpt model
gptmodel.loadModel(model_path='./gpt_model.gpt', progress=True) # loading the pre-trained generative model

prompt = 'What are the main types of machine learning?' # prompt for inference test
gptmodel.print_predict(prompt=prompt, max_tokens=50, stream=True) # infers token by token up to approximately 50 tokens

end = time() # marks the end time
time_spent_gptmodel = abs(start-end) # calculates the time difference between the start and end of execution
print(f'\nRuntime: {time_spent_gptmodel} seconds.') # displays the total time spent in seconds

```
Runned on a Macbook M3 Max with 48GB of VRAM.
```bash
The three main types are:                                                                                                                                       
- **Supervised Learning**: The model learns from labeled data.
- **Unsupervised Learning**: The model identifies patterns without labels.
- **Reinforcement Learning**: The model learns through trial and error, receiving rewards or penalties.

Runtime: 4.383117198944092 seconds.
```
```python
# time measured using model loading delay
from time import time # import time module
start = time() # marks the initial time

from hurmodel import HurModel
hurmodel = HurModel() # instantiation of the transformer class for the hur model
hurmodel.loadModel('./hur_model.gpt') # loading the pre-trained generative model

prompt = 'What are the main types of machine learning?' # prompt for inference test
hurmodel.print_predict(prompt=prompt, max_tokens=50, stream=True) # infers token by token up to approximately 50 tokens

end = time() # marks the end time
time_spent_hurmodel = abs(start-end) # calculates the time difference between the start and end of execution
print(f'\nRuntime: {time_spent_hurmodel} seconds.') # displays the total time spent in seconds

```
Runned on a Macbook M3 Max with 48GB of VRAM.
The **HurModel** network was **2 times** faster in inferring than a conventional Transformer network using the same dataset.
```bash
The three main types are:                                                                                                                                       
- **Supervised Learning**: The model learns from labeled data.
- **Unsupervised Learning**: The model identifies patterns without labels.
- **Reinforcement Learning**: The model learns through trial and error, receiving rewards or penalties.

Runtime: 1.4995019435882568 seconds.
```
Below, check out the comparison of fine-tuning training between a Hur model and a GPT model.
```python
# time measured using model loading delay
from time import time # import time module
start = time() # marks the initial time

gptmodel = GPTModel() # instantiation of the transformer class for the gpt model
gptmodel.loadModel(model_path='./gpt_model.gpt', progress=True) # loading the pre-trained generative model
# applying fine-tuning to the pre-trained model
gptmodel.addFit('What does the acronym GPT mean in language models?', 'GPT in language models stands for Generative Pre-trained Transformer.')
gptmodel.addFit('What is the capital of Spain?', 'The capital of Spain is Madrid.')
# saving the adjusted model
if gptmodel.saveModel(model_path='./adjusted_gpt.gpt'): print('Model with fine-tuned successfully created.')
else: print('ERROR when creating model with fine-tuned!!')

# time measured using model save delay
end = time() # marks the end time
time_spent_gptmodel = abs(start-end) # calculates the time difference between the start and end of execution
print(f'\nRuntime: {time_spent_gptmodel} seconds.') # displays the total time spent in seconds

```
Runned on a Macbook M3 Max with 48GB of VRAM.
```bash
Model with fine-tuned successfully created.                                                                                                                     

Runtime: 4.586612224578857 seconds.
```
```python
# time measured using model loading delay
from time import time # import time module
start = time() # marks the initial time

from hurmodel import HurModel
hurmodel = HurModel() # instantiation of the transformer class for the hur model
hurmodel.loadModel('./hur_model.gpt') # loading the pre-trained generative model
# applying fine-tuning to the pre-trained model
hurmodel.addFit('What does the acronym GPT mean in language models?', 'GPT in language models stands for Generative Pre-trained Transformer.')
hurmodel.addFit('What is the capital of Spain?', 'The capital of Spain is Madrid.')
# saving the adjusted model
if hurmodel.saveModel(model_path='./adjusted_hur.gpt'): print('Model with fine-tuned successfully created.')
else: print('ERROR when creating model with fine-tuned!!')

# time measured using model save delay
end = time() # marks the end time
time_spent_hurmodel = abs(start-end) # calculates the time difference between the start and end of execution
print(f'\nRuntime: {time_spent_hurmodel} seconds.') # displays the total time spent in seconds

```
Runned on a Macbook M3 Max with 48GB of VRAM.
The **HurModel** network was **2 times** faster in fine-tuning than a conventional Transformer network using the same dataset.
```bash
Model with fine-tuned successfully created.                                                                                                                     

Runtime: 1.8265819549560547 seconds.
```

## Contributing

We do not accept contributions that may result in changing the original code.

Make sure you are using the appropriate version.

## License

This is proprietary software and its alteration and/or distribution without the developer's authorization is not permitted.
