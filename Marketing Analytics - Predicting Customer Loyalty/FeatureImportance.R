
rm(list=ls())
#loading csv file
csv_data<- read.csv("D:/vaibhav/Marketing analytics/project/trainfeature.csv")
library(plyr)
library(car)
library(pROC)

dataset<-csv_data
dataset$repeater <- mapvalues(dataset$repeater,c("t","f"),c("1","0"))
dataset[is.na(dataset)]<-0
dataset<-na.omit(dataset) 



dataset$repeater<as.factor(dataset$repeater)
rem<-c("id","offerdate","repeattrips")
dataset=dataset[,!(names(dataset) %in% rem)]

#View(dataset)
model0<-glm(repeater~.,dataset,family='binomial')
summary(model0)
png("InfluencePlot.png")
influencePlot(model0)
dev.off()

remvl<-c("120138","140694")
dataset<-dataset[-120138,]
dataset<-dataset[-140694,]

model0_new<-glm(repeater~.,dataset,family='binomial')

model1<-step(model0_new,direction="both")
model1$anova
anova(model1,test="Chisq")
summary(model1)

SgnfctVars<-summary(model1)$coeff[-1,4]<0.1
(SgnfctVars<-names(SgnfctVars)[SgnfctVars==TRUE])

VIF_vars<-names(vif(model1)[vif(model1)<10])

IndpVars<-intersect(VIF_vars,SgnfctVars)

outpt<-c("repeater")
model2<-glm(repeater~.,data=dataset[,c(outpt,IndpVars)],family='binomial')
summary(model2)


anova(model1,model2)
AIC(model1,model2)
BIC(model1,model2)

anova(model2,test="Chisq")
summary(model2)

SgnfctVars<-summary(model2)$coeff[-1,4]<0.1
(SgnfctVars<-names(SgnfctVars)[SgnfctVars==TRUE])

VIF_vars<-names(vif(model2)[vif(model2)<10])

IndpVars<-intersect(VIF_vars,SgnfctVars)


outpt<-c("repeater")
model3<-glm(repeater~.,data=dataset[,c(outpt,IndpVars)],family='binomial')
summary(model3)

SgnfctVars<-summary(model3)$coeff[-1,4]<0.1
(SgnfctVars<-names(SgnfctVars)[SgnfctVars==TRUE])

VIF_vars<-names(vif(model3)[vif(model3)<10])

IndpVars<-intersect(VIF_vars,SgnfctVars)

coef(model1)
exp(coef(model1))


model1.pre<-predict(model1,type='response')
pre<-ifelse(model1.pre>0.5,1,0)
table(pre,dataset$repeater)
(acc<-sum(diag(table(pre,dataset$repeater)))/1000)


png("roc_curve.png")
modelroc<-roc(dataset$repeater,pre)
plot(modelroc,print.auc=TRUE,auc.polygon=TRUE,grid=c(0.1,0.2),grid.col=c("green","red"),
     max.auc.polygon=TRUE,auc.polygon.col="skyblue",print.thres=TRUE)
dev.off()