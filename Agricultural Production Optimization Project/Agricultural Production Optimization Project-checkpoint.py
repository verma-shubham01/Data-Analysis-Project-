#!/usr/bin/env python
# coding: utf-8

# # Problem statement- 
# ### In this project we will build a predictive model that suggest most suitable crops to grow based on available climate and soil condition  
# # Goal 
# ### Achieve  Precision Forming by optimizing the Agriculture production

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 
from ipywidgets import interact


# In[2]:


dataset=pd.read_csv('Crop_recommendation.csv')
print('Dataset size is :', dataset.shape)


# In[3]:


dataset.head()


# In[4]:


dataset.isnull().sum()


# In[5]:


dataset['label'].value_counts()


# In[6]:


print("Average Ratio of Nitrogen in the soil :", '{:.2f}'.format((dataset['N'].mean())))
print("Average Ratio of Phosphorous in the soil :", '{:.2f}'.format((dataset['P'].mean())))
print("Average Ratio of Potassium in the soil :", '{:.2f}'.format((dataset['K'].mean())))
print("Average Ratio of Temperature in the soil :", '{:.2f}'.format((dataset['temperature'].mean())))
print("Average Ratio of Humidity in the soil :", '{:.2f}'.format((dataset['humidity'].mean())))
print("Average Ratio of PH in the soil :", '{:.2f}'.format((dataset['ph'].mean())))
print("Average Ratio of Rainfall in the soil :", '{:.2f}'.format((dataset['rainfall'].mean())))


# In[7]:


@interact
def cropsummarry(Crops=list(dataset['label'].value_counts().index)):
    x=dataset[(dataset['label']) == Crops]
    print("-----------------------------------------------------")
    print("Statistics for Nitrogen")
    print("Average Nitrogen Required : ", x['N'].mean())
    print("Maximum Nitrogen Required : ", x['N'].max())
    print("Minimum Nitrogen Required : ", x['N'].min())
    print("-----------------------------------------------------")
    
    print("Statistics for Phosphorous")
    print("Average Phosphorous Required : ", x['P'].mean())
    print("Maximum Phosphorous Required : ", x['P'].max())
    print("Minimum Phosphorous Required : ", x['P'].min())
    print("-----------------------------------------------------")
    
    print("Statistics for Potassium")
    print("Average  Potassium Required : ", x['K'].mean())
    print("Maximum Potassium Required : ", x['K'].max())
    print("Minimum Potassium Required : ", x['K'].min())
    print("-----------------------------------------------------")
    
    print("Statistics for temperature")
    print("Average temperature Required : ", x['temperature'].mean())
    print("Maximum temperature Required : ", x['temperature'].max())
    print("Minimum temperature Required : ", x['temperature'].min())
    print("-----------------------------------------------------")
    
    print("Statistics for humidity")
    print("Average humidity Required : ", x['humidity'].mean())
    print("Maximum humidity Required : ", x['humidity'].max())
    print("Minimum humidity Required : ", x['humidity'].min())
    print("-----------------------------------------------------")
    
    print("Statistics for ph")
    print("Average ph Required : ", x['ph'].mean())
    print("Maximum ph Required : ", x['ph'].max())
    print("Minimum ph Required : ", x['ph'].min())
    print("-----------------------------------------------------")
    
    
    print("Statistics for rainfall")
    print("Average rainfall Required : ", x['rainfall'].mean())
    print("Maximum rainfall Required : ", x['rainfall'].max())
    print("Minimum rainfall Required : ", x['rainfall'].min())
    print("-----------------------------------------------------")

    


# In[8]:


@interact
def cropcompare(Conditions =['N','P','K','temperature','ph','humidty','rainfall']):
    print("Average Value for ", Conditions, "is {0:.2f}".format(dataset[Conditions].mean()))
    print("--------------------------------------------------------------")
    print("Rice : {0:.2f}".format(dataset[(dataset['label']=='rice')][Conditions].mean()))
    print("Maize: {0:.2f}".format(dataset[(dataset['label']=='maize')][Conditions].mean()))
    print("Jute : {0:.2f}".format(dataset[(dataset['label']=='jute')][Conditions].mean()))
    print("Cotton: {0:.2f}".format(dataset[(dataset['label']=='cotton')][Conditions].mean()))
    print("Coconut : {0:.2f}".format(dataset[(dataset['label']=='coconut')][Conditions].mean()))
    print("Papaya : {0:.2f}".format(dataset[(dataset['label']=='papaya')][Conditions].mean()))
    print("Orange : {0:.2f}".format(dataset[(dataset['label']=='orange')][Conditions].mean()))
    print("Apple : {0:.2f}".format(dataset[(dataset['label']=='apple')][Conditions].mean()))
    print("Muskmelon : {0:.2f}".format(dataset[(dataset['label']=='muskmelon')][Conditions].mean()))
    print("Watermelon : {0:.2f}".format(dataset[(dataset['label']=='watermelon')][Conditions].mean()))
    print("Grapes : {0:.2f}".format(dataset[(dataset['label']=='grapes')][Conditions].mean()))
    print("Mango : {0:.2f}".format(dataset[(dataset['label']=='mango')][Conditions].mean()))
    print("Banana  : {0:.2f}".format(dataset[(dataset['label']=='banana ')][Conditions].mean()))
    print("Pomegranate : {0:.2f}".format(dataset[(dataset['label']=='pomegranate')][Conditions].mean()))
    print("Lentil : {0:.2f}".format(dataset[(dataset['label']=='lentil')][Conditions].mean()))
    print("Blackgram : {0:.2f}".format(dataset[(dataset['label']=='blackgram')][Conditions].mean()))
    print("Mungbean : {0:.2f}".format(dataset[(dataset['label']=='mungbean')][Conditions].mean()))
    print("Mothbeans : {0:.2f}".format(dataset[(dataset['label']=='mothbeans')][Conditions].mean()))
    print("Pigeonpeas : {0:.2f}".format(dataset[(dataset['label']=='pigeonpeas')][Conditions].mean()))
    print("Kidneybeans : {0:.2f}".format(dataset[(dataset['label']=='kidneybeans')][Conditions].mean()))
    print("Chickpea : {0:.2f}".format(dataset[(dataset['label']=='chickpea')][Conditions].mean()))
    print("Coffee : {0:.2f}".format(dataset[(dataset['label']=='coffee')][Conditions].mean()))
   


# In[10]:


@interact
def cropcompare1(Conditions =['N','P','K','temperature','ph','humidty','rainfall']):
    print('Crops which require greater than average' , Conditions, '\n')
    print(dataset[dataset[Conditions]>dataset[Conditions].mean()]['label'].unique())
    print("------------------------------------------")
    print('Crops which require less than average' , Conditions, '\n')
    print(dataset[dataset[Conditions]<=dataset[Conditions].mean()]['label'].unique())


# In[11]:



plt.subplot(2,4,1)
sns.distplot(dataset['N'], color='darkblue')
plt.xlabel("Ratio of Nitrogen", fontsize=12)
plt.grid()


plt.subplot(2,4,2)
sns.distplot(dataset['P'], color='red')
plt.xlabel("Ratio of Phosphorous", fontsize=12)
plt.grid()


plt.subplot(2,4,3)
sns.distplot(dataset['K'], color='grey')
plt.xlabel("Ratio of Potassium", fontsize=12)
plt.grid()


plt.subplot(2,4,4)
sns.distplot(dataset['temperature'], color='darkred')
plt.xlabel("Ratio of Temperature", fontsize=12)
plt.grid()


plt.subplot(2,4,5)
sns.distplot(dataset['rainfall'], color='green')
plt.xlabel("Ratio of Rainfall", fontsize=12)
plt.grid()


plt.subplot(2,4,6)
sns.distplot(dataset['humidity'], color='lightblue')
plt.xlabel("Ratio of Humidity", fontsize=12)
plt.grid()


plt.subplot(2,4,7)
sns.distplot(dataset['ph'], color='black')
plt.xlabel("Ratio of PH", fontsize=12)
plt.grid()

plt.subplots_adjust(left=.5, bottom=1, right=1.6, top=2, wspace=1,hspace=1)

plt.suptitle('Distribution for Agriculture Conditions',x=1, y=2.2, fontsize=20)
plt.show()



# In[12]:


print("Some Intresting Patterns")
print("---------------------------")
print("crops which requires very high ratio of Nitrogen Content in soil:", dataset[dataset['N']>120]['label'].unique())
print("crops which requires very high ratio of Phosphorous Content in soil:", dataset[dataset['P']>100]['label'].unique())
print("crops which requires very high ratio of Potassium Content in soil:", dataset[dataset['K']>200]['label'].unique())
print("crops which requires very high Rainfall:", dataset[dataset['rainfall']>200]['label'].unique())
print("crops which requires very high Temperature:", dataset[dataset['temperature']>40]['label'].unique())
print("crops which requires very low Temperature:", dataset[dataset['temperature']<10]['label'].unique())
print("crops which requires very low Humidity:", dataset[dataset['humidity']<20]['label'].unique())
print("crops which requires very high PH:", dataset[dataset['ph']>9]['label'].unique())
print("crops which requires very low PH:", dataset[dataset['ph']<4]['label'].unique())


# In[13]:


print("Summer Crops")
print(dataset[(dataset['temperature']> 30) & (dataset['humidity'] > 50)]['label'].unique())
print('-------------------------------------------------')
print("Winter Crops")
print(dataset[(dataset['temperature']< 20) & (dataset['humidity'] > 25)]['label'].unique())
print('-------------------------------------------------')
print("Rainy Crops")
print(dataset[(dataset['rainfall']> 200) & (dataset['humidity'] > 25)]['label'].unique())
print('-------------------------------------------------')
              


# In[14]:


from sklearn.cluster import KMeans
 #remove labels from column
x=dataset.drop(['label'],axis=1)
#select all values of dataset
x=x.values
#checking shape

print(x)
x.dtype


# In[15]:


# Using elbow methode define clusters with in dataset
plt.rcParams['figure.figsize']=(10,4)

wcss=[]
for i in range(1,11):
    km=KMeans(n_clusters=i, init="k-means++",max_iter = 300, n_init=10,random_state=0)
    km.fit(x)
    wcss.append(km.inertia_)
#plot result
plt.plot(range(1,11),wcss)
plt.title('Elbow-Method', fontsize=20)
plt.xlabel('number of cluster')
plt.ylabel("wcss")
plt.show()


# In[ ]:





# In[16]:


#implement of K Means Algorithm
km=KMeans(n_clusters=4, init='k-means++', max_iter =300,n_init = 10,random_state=0)
y_means = km.fit_predict(x)

#find out result
a=dataset['label']
y_means= pd.DataFrame(y_means)
z=pd.concat([y_means,a],axis=1)
z=z.rename(columns={0:"cluster"})

#check the clusters of each crops
print("Let check result after applying K Means clustering Analysis \n")
print("Crops in 1st cluster:",z[z['cluster']==0]["label"].unique())
print("--------------------------------------------------------------")
print("Crops in 2nd cluster:",z[z['cluster']==1]["label"].unique())
print("--------------------------------------------------------------")
print("Crops in 3rd cluster:",z[z['cluster']==2]["label"].unique())
print("--------------------------------------------------------------")
print("Crops in 4th cluster:",z[z['cluster']==3]["label"].unique())
print("--------------------------------------------------------------")


# In[17]:


#split dataset for  predicting modeling
y= dataset["label"]
x=dataset.drop(['label'],axis=1)
print('Shape of x', x.shape)
print('Shape of y', y.shape)


# In[18]:


#create training and testing set for validation of result
from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.15,random_state=0)

print('shape of x_train', x_train.shape)
print('shape of x_test', x_test.shape)
print('shape of y_train', y_train.shape)
print('shape of y_test', y_test.shape)


# In[19]:


from sklearn.linear_model import LogisticRegression
model = LogisticRegression(solver='lbfgs', max_iter=3000)
model.fit(x_train, y_train)
y_pred = model.predict(x_test)


# In[20]:


#evalute model performance
from sklearn.metrics import confusion_matrix
#let print  the confusion matrix
plt.rcParams['figure.figsize'] = (10,10)
cm = confusion_matrix(y_test,y_pred)
sns.heatmap(cm,annot = True, cmap = "Wistia")
plt.title("Confusion Matrix for Logistic Regression", fontsize = 15)
plt.show()


# In[21]:


from sklearn.metrics import classification_report
cr=classification_report(y_test,y_pred)
print(cr)


# In[22]:


#crosscheck for some value
dataset.head()


# In[23]:


prediction=model.predict((np.array([[90,40,40,20,80,7,200]])))
print("The suggested crop for the given Climate Condition is ", prediction)


# In[ ]:




