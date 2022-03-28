**Context**

I participated in this challenge as part of the evaluation of the Machine Learning module during my Post Master's Degree in Big Data (Télécom Paris, 2021-2022).
We were graded on the basis of the individual notebook and our rank among the others 60 students competing.

**Presentation**

How does modern face recognition work?

In the past few years, Face Recognition (FR) systems have reached extremely high levels of performance, paving the way to a broader range of applications, where the reliability levels were previously prohibitive to consider automation. This is mainly due to the adoption of deep learning techniques in computer vision. The most adopted paradigm consists in training a network 

![formula](https://render.githubusercontent.com/render/math?mathf: \mathcal{X} \rightarrow \mathbb{R}^{d})

which, from a given image $i m \in \mathcal{X}$, extracts a feature vector $z \in \mathbb{R}^{d}$ which synthetizes the relevant caracteristics of $i m$. The recognition phase then consists, from two images $i m_{1}, i m_{2}$, to predict wether they correspond to the same identity or not. This is done from the extracted features $z_{1}, z_{2}$.


**Objective** 

In this data challenge, we are asked to train a machine learning model which, from a vector $\left[z_{1}, z_{2}\right]$ made of the concatenation of two templates $z_{1}$ and $z_{2}$, predict wether or not these two images correspond to the same identity.
