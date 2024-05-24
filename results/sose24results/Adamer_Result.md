## Adamer Results
## GIT Statistics 
* **Successful Crawled:** True
* **Has Multiple Branches:** 1
* **Branch Names:** 
main,
 * **Last Updated at:** 2024-05-22T22:46:29.000+02:00
* **Counted Commits in Repo:**
  205
* **Last Build Pipeline Status in Repo:**
  success
  - **Name**: dockerize-demo, **Status**: success, **Stage**: deploy, **Started At**: 2024-05-22T23:24:51.524+02:00
  - **Name**: analyse-demo, **Status**: success, **Stage**: analyse, **Started At**: 2024-05-22T23:12:05.480+02:00
  - **Name**: test-java, **Status**: success, **Stage**: test, **Started At**: 2024-05-22T22:57:16.760+02:00
  - **Name**: build-java, **Status**: success, **Stage**: build, **Started At**: 2024-05-22T22:46:34.546+02:00
* **Missing Keywords in Build Pipeline**: 
build,docker,push,test,sonarqube ,
 ## Required Files 
* **MissingFiles in Repo:**
  ['EXERCISE01/.GITLAB-CI.YML', 'EXERCISE01/DOCKER-COMPOSE.YML']
* **Character Count of Analyse.md:**
  0
## Docker 

 * **Contains all necessary image tags:** True
* **Container Tags:** 
20240414,20240427,20240428,20240430,20240504,20240508,2024_05_14,2024_05_15,2024_05_16,2024_05_17,2024_05_20,2024_05_22,latest,* **Container started successfully:**
  True
* **Good Order Test success?:**
  True
* **Bad Order Test success?:**
  False

 * **Container Logs:** 

		- 11:23:18,409 |-INFO in ch.qos.logback.classic.LoggerContext[default] - This is logback-classic version ?

		- 11:23:18,412 |-INFO in ch.qos.logback.classic.util.ContextInitializer@166fa74d - No custom configurators were discovered as a service.

		- 11:23:18,412 |-INFO in ch.qos.logback.classic.util.ContextInitializer@166fa74d - Trying to configure with ch.qos.logback.classic.joran.SerializedModelConfigurator

		- 11:23:18,424 |-INFO in ch.qos.logback.classic.util.ContextInitializer@166fa74d - Constructed configurator of type class ch.qos.logback.classic.joran.SerializedModelConfigurator

		- 11:23:18,468 |-INFO in ch.qos.logback.classic.LoggerContext[default] - Could NOT find resource [logback-test.scmo]

		- 11:23:18,469 |-INFO in ch.qos.logback.classic.LoggerContext[default] - Could NOT find resource [logback.scmo]

		- 11:23:18,506 |-INFO in ch.qos.logback.classic.util.ContextInitializer@166fa74d - ch.qos.logback.classic.joran.SerializedModelConfigurator.configure() call lasted 45 milliseconds. ExecutionStatus=INVOKE_NEXT_IF_ANY

		- 11:23:18,506 |-INFO in ch.qos.logback.classic.util.ContextInitializer@166fa74d - Trying to configure with ch.qos.logback.classic.util.DefaultJoranConfigurator

		- 11:23:18,507 |-INFO in ch.qos.logback.classic.util.ContextInitializer@166fa74d - Constructed configurator of type class ch.qos.logback.classic.util.DefaultJoranConfigurator

		- 11:23:18,508 |-INFO in ch.qos.logback.classic.LoggerContext[default] - Could NOT find resource [logback-test.xml]

		- 11:23:18,538 |-INFO in ch.qos.logback.classic.LoggerContext[default] - Found resource [logback.xml] at [jar:file:/opt/app/Exercise01-1.0-SNAPSHOT.jar!/logback.xml]

		- 11:23:18,557 |-INFO in ch.qos.logback.core.joran.spi.ConfigurationWatchList@40f08448 - URL [jar:file:/opt/app/Exercise01-1.0-SNAPSHOT.jar!/logback.xml] is not of type file

		- 11:23:19,057 |-INFO in ch.qos.logback.core.model.processor.AppenderModelHandler - Processing appender named [stdout]

		- 11:23:19,058 |-INFO in ch.qos.logback.core.model.processor.AppenderModelHandler - About to instantiate appender of type [ch.qos.logback.core.ConsoleAppender]

		- 11:23:19,313 |-WARN in ch.qos.logback.core.ConsoleAppender[stdout] - This appender no longer admits a layout as a sub-component, set an encoder instead.

		- 11:23:19,313 |-WARN in ch.qos.logback.core.ConsoleAppender[stdout] - To ensure compatibility, wrapping your layout in LayoutWrappingEncoder.

		- 11:23:19,313 |-WARN in ch.qos.logback.core.ConsoleAppender[stdout] - See also http://logback.qos.ch/codes.html#layoutInsteadOfEncoder for details

		- 11:23:19,313 |-INFO in ch.qos.logback.core.model.processor.AppenderModelHandler - Processing appender named [milliroller]

		- 11:23:19,313 |-INFO in ch.qos.logback.core.model.processor.AppenderModelHandler - About to instantiate appender of type [ch.qos.logback.core.rolling.RollingFileAppender]

		- 11:23:19,321 |-WARN in ch.qos.logback.core.rolling.RollingFileAppender[milliroller] - This appender no longer admits a layout as a sub-component, set an encoder instead.

		- 11:23:19,321 |-WARN in ch.qos.logback.core.rolling.RollingFileAppender[milliroller] - To ensure compatibility, wrapping your layout in LayoutWrappingEncoder.

		- 11:23:19,321 |-WARN in ch.qos.logback.core.rolling.RollingFileAppender[milliroller] - See also http://logback.qos.ch/codes.html#layoutInsteadOfEncoder for details

		- 11:23:19,349 |-INFO in c.q.l.core.rolling.TimeBasedRollingPolicy@660879561 - No compression will be used

		- 11:23:19,351 |-INFO in c.q.l.core.rolling.TimeBasedRollingPolicy@660879561 - Will use the pattern logs/datetime-%d{yyyy_MM_dd}.log for the active file

		- 11:23:19,494 |-INFO in c.q.l.core.rolling.DefaultTimeBasedFileNamingAndTriggeringPolicy - The date pattern is 'yyyy_MM_dd' from file name pattern 'logs/datetime-%d{yyyy_MM_dd}.log'.

		- 11:23:19,494 |-INFO in c.q.l.core.rolling.DefaultTimeBasedFileNamingAndTriggeringPolicy - Roll-over at midnight.

		- 11:23:19,526 |-INFO in c.q.l.core.rolling.DefaultTimeBasedFileNamingAndTriggeringPolicy - Setting initial period to 2024-05-24T11:23:19.526Z

		- 11:23:19,551 |-INFO in ch.qos.logback.core.rolling.RollingFileAppender[milliroller] - Active log file name: /logs/output.log

		- 11:23:19,552 |-INFO in ch.qos.logback.core.rolling.RollingFileAppender[milliroller] - File property is set to [/logs/output.log]

		- 11:23:19,554 |-INFO in ch.qos.logback.classic.model.processor.RootLoggerModelHandler - Setting level of ROOT logger to DEBUG

		- 11:23:19,565 |-INFO in ch.qos.logback.core.model.processor.AppenderRefModelHandler - Attaching appender named [stdout] to Logger[ROOT]

		- 11:23:19,574 |-INFO in ch.qos.logback.core.model.processor.AppenderRefModelHandler - Attaching appender named [milliroller] to Logger[ROOT]

		- 11:23:19,574 |-INFO in ch.qos.logback.core.model.processor.DefaultProcessor@588df31b - End of configuration.

		- 11:23:19,575 |-INFO in ch.qos.logback.classic.joran.JoranConfigurator@33b37288 - Registering current configuration as safe fallback point

		- 11:23:19,575 |-INFO in ch.qos.logback.classic.util.ContextInitializer@166fa74d - ch.qos.logback.classic.util.DefaultJoranConfigurator.configure() call lasted 1068 milliseconds. ExecutionStatus=DO_NOT_INVOKE_NEXT_IF_ANY

		- 

		- 11:23:19.601 [main] INFO  org.example.Main - Displaying system information

		- 11:23:19.613 [main] INFO  org.example.Main - PORT: 9500

		- 11:23:19.616 [main] INFO  org.example.Main - Operating System: Linux

		- 11:23:19.616 [main] INFO  org.example.Main - Version: 5.15.146.1-microsoft-standard-WSL2

		- 11:23:19.616 [main] INFO  org.example.Main - User: root

		- 11:23:19.628 [main] INFO  org.example.Main - Host: b1397993116b/172.17.0.2

		- 11:23:19.643 [pool-1-thread-2] INFO  org.example.services.OrderImport - Taking order from input queue.

		- 11:23:19.650 [pool-1-thread-1] INFO  org.example.services.TcpSocket - waiting for client...

		- 11:23:19.655 [pool-1-thread-3] INFO  org.example.services.FileArchiveService - Trying to create subdir: /opt/app/orders/success

		- 11:23:19.662 [pool-1-thread-3] INFO  org.example.services.FileArchiveService - Created subdir /opt/app/orders/success

		- 11:23:19.670 [pool-1-thread-3] INFO  org.example.services.FileArchiveService - Trying to create subdir: /opt/app/orders/failed

		- 11:23:19.686 [pool-1-thread-3] INFO  org.example.services.FileArchiveService - Created subdir /opt/app/orders/failed

		- 11:23:19.687 [pool-1-thread-3] INFO  org.example.services.FileArchiveService - Taking order from output queue...

		- 11:23:20.042 [pool-1-thread-1] INFO  org.example.services.TcpSocket - client connected: /172.17.0.1

		- 11:23:20.044 [pool-1-thread-1] INFO  org.example.services.TcpSocket - waiting for client...

		- 11:23:20.045 [pool-2-thread-1] INFO  org.example.services.TcpSocket - reading transferred client data

		- 11:23:20.046 [pool-2-thread-1] INFO  org.example.services.TcpSocket - Processing read data...

		- 11:23:20.046 [pool-2-thread-1] INFO  org.example.services.TcpSocket - Creating order from transferred data

		- 11:23:20.143 [pool-2-thread-1] INFO  org.example.services.TcpSocket - adding created order to input queue

		- 11:23:20.143 [pool-2-thread-1] INFO  org.example.services.TcpSocket - Done processing received data

		- 11:23:20.144 [pool-1-thread-2] INFO  org.example.services.OrderImport - Retrieved order!

		- 11:23:20.144 [pool-1-thread-2] INFO  org.example.services.OrderImport - Processing order now...

		- 11:23:20.146 [pool-1-thread-2] INFO  org.example.services.OrderImport - processed order!

		- 11:23:20.146 [pool-3-thread-1] INFO  org.example.services.OrderImport - checking order data now...

		- 11:23:20.146 [pool-1-thread-2] INFO  org.example.services.OrderImport - Taking order from input queue.

		- 11:23:20.161 [pool-3-thread-1] INFO  org.example.services.OrderImport - Order is valid checking for promotion!

		- 11:23:20.162 [pool-3-thread-1] INFO  org.example.services.OrderImport - adding to queue for final processing.

		- 11:23:20.163 [pool-3-thread-1] INFO  org.example.services.OrderImport - Adding order to output queue.

		- 11:23:20.163 [pool-3-thread-1] INFO  org.example.services.OrderImport - Successfully added order to queue.

		- 11:23:20.163 [pool-1-thread-3] INFO  org.example.services.FileArchiveService - received order!

		- 11:23:20.163 [pool-1-thread-3] INFO  org.example.services.FileArchiveService - Storing order...

		- 11:23:20.165 [pool-1-thread-3] INFO  org.example.services.FileArchiveService - oder stored!

		- 11:23:20.165 [pool-4-thread-1] INFO  org.example.services.FileArchiveService - Setting customer dir...

		- 11:23:20.165 [pool-1-thread-3] INFO  org.example.services.FileArchiveService - Taking order from output queue...

		- 11:23:20.165 [pool-4-thread-1] INFO  org.example.services.FileArchiveService - customer dir was set.

		- 11:23:20.165 [pool-4-thread-1] INFO  org.example.services.FileArchiveService - Setting filename...

		- 11:23:20.169 [pool-4-thread-1] INFO  org.example.services.FileArchiveService - filename was set.

		- 11:23:20.169 [pool-4-thread-1] INFO  org.example.services.FileArchiveService - Trying to create subdir: /opt/app/orders/success/Mustermann

		- 11:23:20.170 [pool-4-thread-1] INFO  org.example.services.FileArchiveService - Created subdir /opt/app/orders/success/Mustermann

		- 11:23:20.171 [pool-4-thread-1] INFO  org.example.services.FileArchiveService - Trying to create and write to file 2024-05-17_15-45-00.json.

		- 11:23:20.181 [pool-4-thread-1] INFO  org.example.services.FileArchiveService - Created File for Order with ID ORD12345.

		- 11:23:20.182 [pool-4-thread-1] INFO  org.example.services.FileArchiveService - Created file can be found under: /opt/app/orders/success/Mustermann/2024-05-17_15-45-00.json

		- 11:23:22.904 [pool-1-thread-1] INFO  org.example.services.TcpSocket - client connected: /172.17.0.1

		- 11:23:22.905 [pool-1-thread-1] INFO  org.example.services.TcpSocket - waiting for client...

		- 11:23:22.906 [pool-2-thread-2] INFO  org.example.services.TcpSocket - reading transferred client data

		- 11:23:22.907 [pool-2-thread-2] INFO  org.example.services.TcpSocket - Processing read data...

		- 11:23:22.907 [pool-2-thread-2] INFO  org.example.services.TcpSocket - Creating order from transferred data

		- 11:23:22.947 [pool-2-thread-2] WARN  org.example.services.TcpSocket - Exception during Json Processing: Cannot invoke "org.example.models.Customer.getName()" because the return value of "org.example.models.Order.getCustomer()" is null

		- java.lang.NullPointerException: Cannot invoke "org.example.models.Customer.getName()" because the return value of "org.example.models.Order.getCustomer()" is null

		- 	at org.example.services.TcpSocket.createOrder(TcpSocket.java:58)

		- 	at org.example.services.TcpSocket.handleClient(TcpSocket.java:46)

		- 	at org.example.services.TcpSocket.lambda$startSocket$0(TcpSocket.java:32)

		- 	at java.base/java.util.concurrent.ThreadPoolExecutor.runWorker(Unknown Source)

		- 	at java.base/java.util.concurrent.ThreadPoolExecutor$Worker.run(Unknown Source)

		- 	at java.base/java.lang.Thread.run(Unknown Source)

		- 11:23:22.950 [pool-2-thread-2] INFO  org.example.services.TcpSocket - Done processing received data
