pipeline {
  agent any

  stages {
    stage('Checkout repository') {
      steps {
        checkout scm
      }
    }

    stage('Build Docker Image && Create containers') {
      steps {
        withCredentials([
          string(credentialsId:'Gruzin-docker_registry_access', usernameVariable: 'GITEA_USER', passwordVariable: 'GITEA_TOKEN')]){
          sh 'docker login git gruzin.host -u $GITEA_USER -p $GITEA_PASSWORD'
          sh 'docker build -t gruzin.host/Gruzin/bonk-bot:latest'
        }
      }
    }

    stage('Publish Docker Image') {
      steps {
          sh 'docker push gruzin.host/Gruzin/bonk-bot:latest'
      }
    }
  }
}


