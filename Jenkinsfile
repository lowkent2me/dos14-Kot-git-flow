pipeline {
  agent any
    stages {
      stage('Lint') {
        agent {
            docker {
                image 'python:3.11.3-buster'
                args '-u 0'
            }
        }
        when {
          anyOf {
            branch pattern: "feature*"
            branch pattern: "fix*"
          }
        }
        steps {
          sh "pip install poetry"
          sh "poetry install --with dev"
          sh "poetry run -- black --check *.py"
        }
      }
      stage('Build') {
      when {
        anyOf {
          branch pattern: "master"
        }
      }
      steps {
        script {
          def image = docker.build "lowkent2me/bank:${env.GIT_COMMIT}"
          docker.withRegistry('','dockerhub-kvs') {
            image.push()
          }
        }
      }
    }
    stage('Update Helm Chart') {
      when {
        anyOf {
          branch pattern: "feature-CD"
          branch pattern: "master"
        }
      }
      steps {
        sh 'sed -E 's/tag:.+$/tag: '"$GIT_COMMIT"'/g' k8s/bank/values.yaml'
        sh "cat k8s/bank/values.yaml"
      }
    }
  }
}
