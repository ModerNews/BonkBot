pipeline {
  agent any

  stages {
    stage('Checkout repository') {
      steps {
        checkout scm
      }
    }

    stage('Build Docker Image') {
      steps {
        sh 'docker compose create' 
      }
    }

    stage('Run Docker Image') {
      steps {
        withCredentials([string(credentialsId:'Discord_Mash',variable:'DISCORD_TOKEN')]){
          sh 'docker compose up -d'
        }
      }
    }
  }
}

