# lsfusion-samples

[project]:https://github.com/mazzy-ax/lsfusion-samples
[license]:https://github.com/mazzy-ax/lsfusion-samples/blob/master/LICENSE
[lsFusion]:https://lsfusion.org/
[docpage]:https://documentation.lsfusion.org/pages/viewpage.action?pageId=2228236
[git]:https://git-scm.com/download/
[docker]:https://docs.docker.com/install/
[docker-compose]:https://docs.docker.com/compose/install/
[IntelliJ IDEA]:https://www.jetbrains.com/idea/
[pgadmin]:https://www.pgadmin.org/

<img alt="logo" src="https://lsfusion.org/themes/lsfusion/assets/images/i-logo-lsfusion.svg" align="right">

Примеры для демонстрации возможностей платформы [lsFusion]. Описание [здесь][docpage]. 

Проект [lsfusion-samples][project] должен упростить жизнь тем, кто только начал знакомиться с [lsFusion].
Предполагается, что перед началом работы с примерами вы запускаете сервисы одной командой `docker-compose`,
а дальше работаете только внутри [IntelliJ IDEA].

Причем проект устроен так, что вам не нужно изучать и использовать maven-команды,
достаточно запускать конфигурации нужных вам модулей в [IntelliJ IDEA].

Оглавление:

* [Windows](#Windows)
* [Linux](#Linux)
  * [Необходимо установить](#Необходимо-установить)
  * [Как запустить lsFusion в браузере](#Как-запустить-lsFusion-в-браузере)
  * [Необходимо установить для desktop-клиента lsFusion](#Необходимо-установить-для-desktop-клиента-lsFusion)
  * [Как запустить desktop-клиент](#Как-запустить-desktop-клиент)
* [Дополнительно для Linux](#Дополнительно-для-Linux)
  * [Docker plugin для IntelliJ IDEA](#Docker-plugin-для-IntelliJ-IDEA)
  * [Как запустить pgadmin в браузере](#Как-запустить-pgadmin-в-браузере)

## Windows 

В Windows используйте специальный [установщик](https://documentation.lsfusion.org/pages/viewpage.action?pageId=57738076),
который автоматически установит все необходимое для работы с демонстрационными примерами и создаст иконки для запуска.

Скачайте и распакуйте ZIP-файл из проекта [lsfusion-samples][project] в каталог на своем компьютере,
откройте этот каталог в [IntelliJ IDEA], выберите интерсную вам конфигурацию и запустите ее в [IntelliJ IDEA].

Щелкните мышкой на иконку desktop-клиента или откройте в браузере страницу по адресу <http://localhost:8080>.  

## Linux

В Linux нужно выполнить [несколько шагов](https://documentation.lsfusion.org/pages/viewpage.action?pageId=57738076),
чтобы установить необходимое для промышленной эксплуатации. 
 
Данный проект предназначен для тех, кто начинает изучать [lsfusion]. Поэтому проект содержит `docker-compose.yml`,
который значительно упрощает установку [lsFusion] в Linux на компьютер разработчика.

Примечание: данный проект тестировался на Ubuntu 18.04.

### Необходимо установить

Прежде всего, вам нужно установить базовые вещи:

* [git]
* [docker]
* [docker-compose]
* [IntelliJ IDEA]

  <details>
  <summary>
  Примечания:
  </summary>
  
  1. Для работы с демонстрационными примерами достаточно установить `Community Edition`
  1. На Ubuntu `IDEA Community Edition` можно найти в штатной утилите `Ubuntu software`
     или установить безо всяких заморочек через `snap`:

     ```
     sudo snap install intellij-idea-community --classic 
     ```
     
  </details>
     
* [lsFusion plugin](https://plugins.jetbrains.com/plugin/7601-lsfusion/) для [IntelliJ IDEA]

  <details>
  <summary>
  Как установить:
  </summary>

  * откройте `File \ Settings \ Plugins` в `IDEA`
  * найдите плагин `lsFusion` и нажмите `Install`
    
  </details>

### Как запустить [lsFusion] в браузере

1. склонируйте проект на свой компьютер

    ```
    $ git clone https://github.com/mazzy-ax/lsfusion-samples.git
    ```

1. войдите в каталог проекта `lsfusion-samples`
1. выполните команду `docker-compose up -d` чтобы запустить сервер базы данных и `lsFusion-client`

    ```
    $ cd lsfusion-samples
    $ docker-compose up -d
    ```

1. откройте каталог проекта в `IntelliJ IDEA`

   * разрешите maven'у открыть pom.xml и синхронизировать зависимости
   * обязательно дождитесь пока maven загрузит все зависимости
   * иногда приходится делать повторную команду на синхрониацию зависимостей - нажмите `Reimport All Maven Projects` в окне `Maven`
   * перед первым билдом укажите Project SDK, который предпочитаете (File \ Project Structure \ Project Settings \ Project \ Project SDK)
    
1. выберите конфигурацию с примером. Например, `lsFusion server: hockeystats` (Run \ Edit configurations...)
1. запустите эту конфигурацию (Run \ Run 'lsFusion server: hockeystats')
1. откройте в браузере страницу по адресу <http://localhost:8080>

### Необходимо установить для desktop-клиента [lsFusion]

* установите ПО из раздела [Необходимо установить](#Необходимо-установить)

* [java](https://www.java.com) 8+

  <details>
  <summary>
  Примечание:
  </summary>
    
  в `Ubuntu` достаточно выполнить команду:
    
    ```
    sudo apt install default-jdk
    ```
    
  </details>
    
* (опционально) [IceTea Web Control](https://icedtea.classpath.org/wiki/IcedTea-Web) для запуска desktop-клиента [lsFusion] по jnlp-ссылке

  <details>
  <summary>
  Примечание:
  </summary>

  `IceTea Web Control` &mdash; это проект, который позволяет запускать
  Java-апплеты при помощи jnlp-ссылок.

  В [IntelliJ IDEA] выберите интересную вам конфигурацию и запустите выполнение.
  [IntelliJ IDEA] начнет компиляцию и build модуля [lsFusion].
  Когда билд модуля подходит к концу, в log пишется jnlp-ссылка
  на desktop-клиента. Если нажать на нее, то `IceTea Web Control` автоматически запустит desktop-клиент.
  
  Если не установить `IceTea Web Control`, то desktop-клиент придется запускать вручную.

  </details>

  <details>
  <summary>
  Как установить:
  </summary>

  Инструкции по установке можно найти на сайте проекта [IceTea Web Control](https://icedtea.classpath.org/wiki/IcedTea-Web).
  На Ubuntu можно найти и установить в штатной утилите `Ubuntu software`. 

  Вы можете убрать назойливый splash, задав переменные окружения:

    ```
    ICEDTEA_WEB_PLUGIN_SPLASH=none
    ICEDTEA_WEB_SPLASH=none
    ```

  </details>

* (опционально) `jar-файл` с desktop-клиентом [lsFusion]

  <details>
  <summary>
  Как использовать:
  </summary>

  * Скачайте desktop-клиент [lsFusion] версии 2.1 по ссылке: <https://download.lsfusion.org/java/lsfusion-client-2.1.jar>
  * Войдите в каталог, куда сачали файл, и выполните команду `java -jar lsfusion-client-2.1.jar`
  * Чтобы скачанный файл можно было запускать щелчком мышки, сделайте скачанный файл исполняемым (executable) командой `chmod +x lsfusion-client-2.1.jar`

  </details>

### Как запустить desktop-клиент

1. склонируйте проект на свой компьютер:

    ```
    $ git clone https://github.com/mazzy-ax/lsfusion-samples.git
    ```

1. войдите в каталог проекта `lsfusion-samples`
1. выполните команду `docker-compose up -d` чтобы запустить сервер базы данных и `lsFusion-client`

    ```
    $ cd lsfusion-samples
    $ docker-compose up -d
    ```

1. откройте каталог проекта в `IntelliJ IDEA`

   * разрешите maven'у открыть pom.xml и синхронизировать зависимости
   * обязательно дождитесь пока maven загрузит все зависимости
   * иногда приходится делать повторную команду на синхрониацию зависимостей - нажмите `Reimport All Maven Projects` в окне `Maven`
   * перед первым билдом укажите Project SDK, который предпочитаете (File \ Project Structure \ Project Settings \ Project \ Project SDK)
    
1. выберите конфигурацию с примером. Например, `lsFusion server: hockeystats` (Run \ Edit configurations...)
1. запустите эту конфигурацию (Run \ Run 'lsFusion server: hockeystats')
1. запустите desktop-клиент:

   * если у вас установлен `IceTea Web Control`, то кликните на jnlp-ссылку, которая появится в конце build-лога в информационном окне `Run`
   * или запустите `jar-файл` с desktop-клиентом lsFusion


## Дополнительно для Linux

### Docker plugin для [IntelliJ IDEA]

[Docker plugin](https://plugins.jetbrains.com/plugin/7724-docker/) позволяет работать с докером непосредственно из [IntelliJ IDEA].
Плагин уже включен в `Ultimate edition`. В `IDEA Community edition` его нужно установить.

  <details>
  <summary>
  Как установить:
  </summary>

  * откройте `File \ Settings \ Plugins` в `IDEA`
  * найдите плагин `Docker` и нажмите `Install`
    
  </details>

### Как запустить [pgadmin] в браузере

Прежде всего склонируйте проект на свой компьютер:

```
$ git clone https://github.com/mazzy-ax/lsfusion-samples.git
```

Затем:

1. войдите в каталог проекта `lsfusion-samples`
1. выполните команду `docker-compose up -d` чтобы запустить сервер базы данных и `lsFusion-client`

    ```
    $ cd lsfusion-samples
    $ docker-compose up -d
    ```

1. откройте в браузере страницу по адресу <http://localhost:5050>
1. в первый раз [pgadmin] спросит email и пароль администратора.

   * введите email: `pgadmin4@pgadmin.org`
   * введите пароль: `11111`
   
1. в первый раз `pgadmin` автоматически добавит сервер с базой данных и попросит пароль администратора `postgres`

   * введите пароль: `11111`
   * если хотите, установите галочку `Save password`
