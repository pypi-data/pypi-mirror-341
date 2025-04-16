X<-c(152,156,159,163,165)
Y<-c(63,68,59,71,64)
X
Y
relationYX<-lm(Y~X)
print(relationYX)

relationXY<-lm(X~Y)
print(relationXY)

summaryXY=summary(relationXY)
print(summaryXY)

summaryYX=summary(relationYX)
print(summaryYX)

 print(summaryYX)

a=data.frame(X=173)
result=predict(relationYX,a)
print(paste("Weight of the student when Height=173 is ",result," kg"))
b=data.frame(Y=70)
result1=predict(relationXY,b)

print(paste("Height of the student when weight=70 is ",result1," cm"))
plot(Y,X,col="blue",main="Height and Weight of Students",xlab="Weight",ylab="Height",pch=15,abline(lm(X~Y)))



a=mtcars[c("cyl","wt","am","gear")]
d=head(a)
d
b<-glm(formula=am~cyl+wt,data=a,family=binomial)
c<- summary(b)
c
