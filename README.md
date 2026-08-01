# t_kyn_communal_the_test
Public Test

A module will be created to test various functions.

* Objectives
  * In recent years, businesses have been required to undergo transformation.
  * One aspect of this is the increasing number of companies pushing for DX (Digital Transformation) strategies.
  * Alongside personal skill development in areas of expertise, there is a need to relearn new knowledge.
  * Speed up the trial-and-error process of system development.
  * Rapidly create systems to test ideas as they arise.
  * github actions
    * Test new features that may incur costs in private repositories.
    * Test the use of LocalStack to simulate AWS services locally.
    * Test the use of Local Terraform to manage infrastructure as code.

* Preconditions
  * Personal information is prohibited from being uploaded.
  * Data will be either open data or generated using Faker.
  * The goal is to rapidly create systems as ideas come up.
  * If not using Github Actions:
  * Use Visual Studio Code for development.

* Content Being Developed
  * **1) Django Application Development**
    * **CAUTION: This project is currently a lower priority, so updates may be infrequent.**
    * Operation Flow
      * Develop Django applications using Visual Studio Code.
      * Commit and upload to a Github repository.
      * Perform functionality checks on Google Colaboratory.
      * The flow for rapid development will be: Visual Studio Code → Github → Google Colaboratory.
      * Specific file used on Google Colaboratory:
        * django_hogehogehogeeeeeeeeee.ipynb
    * Applications
      * Utilizing open data (under consideration). (✅)
      * Picture book viewer (❌)
      * Sample EC site as python application, typescript, etc. (❌)
      * Use as an album server (**Currently working on acclaim**) (❌)
          * content/t_kyn_test_app/django_preinstall.sh
            * pip install django
          * python content/t_kyn_test_app/manage_t_kyn.py runserver
            * execute the python applications.
      * chat tool (almost ✅)
        * Not probably realtime message exchange
      * Todo management（✅）
        * title and text descriptions.
      * Map Location Recording（✅）
      * Drawing tool (❌)
      * spreadsheet making tool (❌)
      * stock invest analyze tool (❌)
      * cooking recipe viewer (❌)

  * **2) Web Hosting Development**
    * Functionality checks for HTML, CSS, and JavaScript.
    * Use as public news site (under consideration).
    * This also serves as a platform for recording and sharing knowledge related to childcare, household tasks, and daily life.

  * **3) Testing New Features in Github Actions**
    * Trial development of features that may incur costs in repositories.
    * Develop and validate various automation features that can be safely made public.
    * **This is a only public repository, so the Github Actions of private repositories is trade secret.**

* Notes
  * There are many possibilities:
    * Running LocalStack with Github Actions.
      https://qiita.com/damepo9696/items/fcf2af605b45bdf07b1a
    * Running LocalStack with Github Actions + Terraform.
      https://medium.com/@robbiedouglas/using-localstack-and-github-actions-to-test-terraform-aws-deployments-0a119dcff7c2
    * Using LocalStack with Terraform.
      https://dev.classmethod.jp/articles/terraform-localstack/
  * Caution
    * Above as said, personal information is prohibited from being uploaded.
    * The development way is as follows:
      * Visual Studio Code → Github → Google Colaboratory.
      * Using Google AI studio to check functionality.
      * Code Assistants of Github Copilot are used.
    * If not using Github Actions:
      * Use Visual Studio Code for development.