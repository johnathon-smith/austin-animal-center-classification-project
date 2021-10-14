# Austin Animal Center: Intakes and Outcomes

By: Johnathon Smith

Date: Oct 13, 2021
***

### Executive Summary
***

__Project Goal__

The goal of this project is to reduce the euthanization of healthy animals. Since the Austin Animal Center only euthanizes healthy animals when the shelter is full, I performed time-series analysis on the number of animal intakes since October 1st, 2013. By searching for trends and repetitive cycles, I had hoped to provide recommendations to keep the shelter from reaching max capacity.

__Overall Findings__

* A cyclic trend definitely exists for animal intakes and adoptions. The euthanization rate has slowly decreased over time.
* At the start of the Covid-19 pandemic in early 2020, there was a sharp decline in numbers for all categories other than number of euthanizations. Since that time, numbers for those categories have started to rise again.
* Animal intake and adoption counts are expected to continue rising and return to pre-pandemic numbers. 

__Recommendations__

To minimize the euthanization of healthy animals, I recommend:

* Transferring eligible animals currently housed at the shelter to other 'No-Kill' shelters in the Austin area.
* Promoting and encouraging adoptions with a strong marketing plan.
* Promoting and encouraging the fostering of animals.

The purpose of these recommendations is to reduce the number of animals currently housed at the shelter. This will help prevent the rising number of animal intakes from overwhelming the Austin Animal Center and reduce the risk of having to euthanize healthy animals.
***

#### Deliverables
* A five minute verbal presentation.
* A Github Repository containing:
    - A clearly labeled final report jupyter notebook.
    - The .py files necessary to reproduce my work.
    - The .csv files necessary to reproduce my work.
* Finally, a README.md file documenting my project planning with instructions on how someone could clone and reproduce my project on their own machine. Goals for the project, a data dictionary, and key findings and takeaways should be included.

#### Context
* The Austin Animal Center data I'm using was acquired from the Austin Open Data Portal. The data is current as of October 10th, 2021.

#### Data Dictionary (Relevant Columns Only)
__Data Dictionary__

| Feature | Datatype | Definition |
|:--------|:---------|:------------|
| intakes | int | The number of animals received by the Austin Animal Center|
| adoptions | int | The number of animals adopted from the Austin Animal Center |
| euthanizations | int | The number of animals (Healthy or otherwise) euthanized at the Austin Animal Center |
| transfers | int | The number of animals transferred to partner programs or shelters in Austin |

***

### My Process
***

##### Trello Board
 - https://trello.com/b/4yQhB5f2/austin-animal-center-tsa


##### Plan
- [x]Write a README.md file that details my process, my findings, and instructions on how to recreate my project.
- [x]Acquire the Ausin Animal Center data from the Austin Open Data Portal.
- [x]Clean and prepare the Austin Animal Center data:
    * There are two different data sets I had to use: Intakes and Outcomes
    * Prepare each individually
    * Create a common datetime index between the two of them
    * Merge them together
- [x]Plot individual variable distributions
- [x]Explore the data and look for long term trends and cyclic behavior.
- [x]Set baseline using the Simple Average.
- [x]Create and evaluate models on train and validate sets.
- [x]Choose best model and evaluate it on test data set.
- [x]Document conclusions, takeaways, and next steps in the Final Report Notebook.

___

##### Plan -> Acquire / Prepare
* Create and store functions needed to acquire and prepare the Austin Animal Center data in a wrangle.py file.
* Import the wrangle.py module and use it to acquire the data in the Final Report Notebook.
* Complete some initial data summarization (`.info()`, `.describe()`, ...).
* Plot distributions of individual variables.
* List key takeaways.

___

##### Plan -> Acquire / Prepare -> Explore
* Create visuals that will help discover long term trends or cyclic behavior over time.
* List key takeaways.

___

##### Plan -> Acquire / Prepare -> Explore -> Model / Evaluate
* Set a baseline using the Simple Average.
* Create and evaluate at least four models.
* Choose best model and evaluate it on the test data set.
* Document conclusions and next steps.

***

### Reproduce My Project

***

- [x] Read this README.md
- [ ] Download the final report Jupyter notebook.
- [ ] Download the wrangle.py, explore.py, and model.py modules into your working directory.
- [ ] Download the 'Austin_Animal_Center_Intakes' and 'Austin_Animal_Center_Outcomes' .csv files into your working directory.
- [ ] Run the final report Jupyter notebook.