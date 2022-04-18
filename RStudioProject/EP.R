data <- read.csv("C:/Users/gelen/Desktop/ECN 190/tipping/tips.csv")

library(ggplot2)
head(data)
sextip <- tapply(data$tip, data$sex, mean)
sextip
smokertip <- tapply(data$tip, data$smoker, mean)
smokertip
daytip <- tapply(data$tip, data$day, mean)
daytips
timetip <- tapply(data$tip, data$time, mean)
timetip
sizetip <- tapply(data$tip, data$size, mean)
sizetip
cr <- as.array(timetip, sizetip, data =data)
cr

c(sextip, smokertip, daytip, timetip, sizetip)

#mean and standard deviation
c(mean(data$tip), sd(data$tip), sqrt(var(data$tip)/dim(data)[1]))

#confidence interval at 95% level
mean(data$tip)+c(-1,1)*1.96*sqrt(var(data$tip)/dim(data)[1])

#bootstrap for standard deviation
bs <- c()
for (b in 1:500){
  samp_b = sample.int(dim(data)[1], replace = TRUE)
  xbar_b = mean(data$tip[samp_b])
  bs = c(bs, xbar_b)
}
sd(bs)

#bootstrape for confidence interval
mean(data$tip)+c(-1,1)*1.96*sd(bs)

#The elasticity for each day in a week
brandcol <-c("green","red","yellow","blue")
par(mfrow=c(1,2))
plot(log(tip)~size, data=data, col=brandcol)
plot(log(tip)~ log(total.bill), data=data, col=brandcol[data$day])

par(mfrow=c(1,2))
plot(log(tip)~time, data=data, col=brandcol)
plot(log(tip)~ log(size), data=data, col=brandcol[data$size])


#linear regression

#getting into model matrix
data[c(80,160,240),]
x <- model.matrix(~log(total.bill)+day, data=data)
x[c(80,160,240),]

#plot the elasticity
beta <-coef(reg2)
plot(log(tip)~ log(total.bill), data=data, col=brandcol[data$day],
     cex=.1, pch=20, bty="n")
abline(a=beta[1], b=beta[2], col=brandcol[1], lwd=2)
abline(a=beta[1]+beta[3], b=beta[2], col=brandcol[2], lwd=2)
abline(a=beta[1]+beta[4], b=beta[2], col=brandcol[3], lwd=2)
abline(a=beta[1]+beta[5], b=beta[2], col=brandcol[4], lwd=2)
legend("bottomleft", bty="n", lwd=2, col=brandcol, legend=levels(data$day))

beta2 <-coef(reg3)
plot(log(tip)~ log(total.bill), data=data, col=brandcol[data$time],
     cex=.1, pch=20, bty="n")
abline(a=beta2[1], b=beta2[2], col=brandcol[1], lwd=2)
abline(a=beta2[1]+beta2[3], b=beta2[2], col=brandcol[2], lwd=2)
legend("bottomleft", bty="n", lwd=2, col=brandcol, legend=levels(data$time))
#adding the interaction
reg_interact <- glm(log(tip)~log(total.bill)*day, data=data)
coef(reg_interact)
reg_interact2 <- glm(log(tip)~log(total.bill)*time, data=data)
coef(reg_interact2)
reg_interact3 <- glm(log(tip)~log(total.bill)+day+time+log(total.bill)*day+log(total.bill)*time,data=data)
coef(reg_interact3)

#we plot the graph again
beta3 <-coef(reg_interact)
plot(log(tip)~ log(total.bill), data=data, col=brandcol[data$day],
     cex=.1, pch=20, bty="n")
abline(a=beta3[1], b=beta3[2], col=brandcol[1], lwd=2)
abline(a=beta3[1]+beta3[3], b=beta3[2], col=brandcol[2], lwd=2)
abline(a=beta3[1]+beta3[4], b=beta3[2], col=brandcol[3], lwd=2)
abline(a=beta3[1]+beta3[5], b=beta3[2], col=brandcol[4], lwd=2)
legend("bottomleft", bty="n", lwd=2, col=brandcol, legend=levels(data$day))

beta4 <-coef(reg_interact)
plot(log(tip)~ log(total.bill), data=data, col=brandcol[data$time],
     cex=.1, pch=20, bty="n")
abline(a=beta4[1], b=beta4[2], col=brandcol[1], lwd=2)
abline(a=beta4[1]+beta4[3], b=beta4[2], col=brandcol[2], lwd=2)
legend("bottomleft", bty="n", lwd=2, col=brandcol, legend=levels(data$time))

#now we are getting into logistic field
reg4 <- glm(log(tip)~smoker+sex+size, data =data)
beta5 <- coef(reg4)

plot(log(tip)~smoker+sex+size, data =data, col=brandcol[data$size])
abline(a=beta5[1], b=beta5[2], col=brandcol[1], lwd=2)
abline(a=beta5[1]+beta5[3], b=beta5[2], col=brandcol[2], lwd=2)
abline(a=beta5[1]+beta5[4], b=beta5[2], col=brandcol[3], lwd=2)
abline(a=beta5[1]+beta5[5], b=beta5[2], col=brandcol[4], lwd=2)
legend("bottomleft", bty="n", lwd=2, col=brandcol, legend=levels(data$day))

#let's get the oos now
library(gamlr)
library(Matrix)

reg2 <- glm(tip~total.bill+smoker+sex+day+time+size+smoker*sex+total.bill*size+total.bill*day+total.bill*time+size*day+size*time,data=data)
summary(reg2)

full <- glm(tip~.,data=data)
summary(full)

1-full$deviance/full$null.deviance
1-reg2$deviance/reg2$null.deviance


#get the p-value now
pvals <- summary(full)$coef[-1,4]
pvals2 <- summary(reg2)$coef[-1,4]

#
signif<- which(pvals <= quantile(pvals, 25/100))
cutvar <- c("tip", names(signif))
cut <- glm(tip~.,data = data[cutvar])

signif2<- which(pvals2 <= quantile(pvals2, 25/450))
cutvar2 <- c("tip", names(signif2))
cut2 <- glm(tip~.,data = data[cutvar2])

1-cut$deviance/cut$null.deviance
1-cut2$deviance/cut2$null.deviance
#
n <- nrow(data)
K <- 10
foldid <- rep(1:K, each=ceiling(n/K))[sample(1:n)]
foldid[1:20]

#
OOS <- data.frame(full=rep(NA,K), cut=rep(NA,K))
for(k in 1:K){
  train <- which(foldid != K)
  rfull <- glm(tip~., data=data, subset = train)
  rcut <- glm(tip~.,data=data[,cutvar], subset=train)
  predfull <- predict(rfull, newdata=data[-train,],type="response")
  predcut <- predict(rcut, newdata=data[-train,],type="response")
  devfull = sum((data$tip - predfull)^2)
  dev0full = sum((data$tip - mean(data$tip))^2)
  OOS$full[k] <- 1-devfull/dev0full
  devcut = sum((data$tip - predcut)^2)
  dev0cut = sum((data$tip - mean(data$tip))^2)
  OOS$cut[k] <- 1-devcut/dev0cut
}
colMeans(OOS)
minioops = which.min(colMeans(OOS))
minioops

#
n2 <- nrow(data)
K2 <- 10
foldid2 <- rep(1:K2, each=ceiling(n2/K2))[sample(1:n2)]

foldid2[1:30]

#
OOS2 <- data.frame(reg2=rep(NA,K2), cut2=rep(NA,K2))
for(k2 in 1:K2){
  train2 <- which(foldid != K2)
  rfull2 <- glm(tip~total.bill+smoker+sex+day+time+size+smoker*sex+total.bill*size+total.bill*day+total.bill*time+size*day+size*time,data=data, subset = train2)
  rcut2 <- glm(tip~.,data=data[,cutvar2], subset=train2)
  predfull2 <- predict(rfull2, newdata=data[-train2,],type="response")
  predcut2 <- predict(rcut2, newdata=data[-train2,],type="response")
  devfull2 = sum((data$tip - predfull2)^2)
  dev0full2 = sum((data$tip - mean(data$tip))^2)
  OOS2$reg2[k2] <- 1-devfull2/dev0full2
  devcut2 = sum((data$tip - predcut2)^2)
  dev0cut2 = sum((data$tip - mean(data$tip))^2)
  OOS2$cut2[k2] <- 1-devcut2/dev0cut2
}
colMeans(OOS2)
minioops2 = which.min(colMeans(OOS2))
minioops2

#Lasso

X=model.matrix(reg2)
XX=model.matrix(full)

cv.tip = cv.gamlr(X, log(data$tip), nlambda = 100, lambda.start = Inf, lambda.min.ratio = 0.001)
cv.tip2 = cv.gamlr(XX, log(data$tip),nlambda = 100, lambda.start = Inf, lambda.min.ratio = 0.001)
plot(cv.tip$gamlr)
plot(cv.tip)
plot(cv.tip2$gamlr)
plot(cv.tip2)


betamin <- coef(cv.tip, select = "1se")
betami

