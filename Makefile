init:
	git init
	python -m venv myenv
	echo myenv > .gitignore
activate:
	myenv\Scripts\activate
install:
	pip install -r requirements.txt
login:
	aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 478259563916.dkr.ecr.us-east-1.amazonaws.com
docker:
	docker build -t awsservices .
tag:
	docker tag awsservices:latest 478259563916.dkr.ecr.us-east-1.amazonaws.com/awsservices:latest
push: 
	docker push 478259563916.dkr.ecr.us-east-1.amazonaws.com/awsservices:latest

aws: login docker tag push

run: 
	myenv\Scripts\activate
	python api.py
