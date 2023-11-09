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
          script { build = false }
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
          build = "${env.GIT_COMMIT}"
          }
        }
      }
    }
    stage('Update Helm Chart') {
      when {
        expression {
          build == "${env.GIT_COMMIT}" &&  "${env.BRANCH_NAME}" == "master"
        }
       }
      steps {
        sh "git checkout feature-CD"
        sh "git config --global pull.rebase true"
        sh "git pull origin"
        script {
        def filename = 'k8s/bank/values-prd.yaml'
        def data = readYaml file: filename

        // Change something in the file
        data.image.tag = "${env.GIT_COMMIT}"

        sh "rm $filename"
        writeYaml file: filename, data: data

          withCredentials([string(credentialsId: 'kvs_github_token', variable: 'SECRET')]) {
                sh('git config --global user.email "vitalikot1996@gmail.com" && git config --global user.name "Jenkins"')
                sh('git add .')
                sh('git commit -m "JENKINS: add new image tag ("${env.GIT_COMMIT}") tag in helm chart tag for CD"')
                sh('git remote set-url origin https://${SECRET}@github.com/lowkent2me/dos14-Kot-git-flow.git')
                sh('git push')
          }
        }
      }
    }
  }
}
