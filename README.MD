<h2>Телеграм бот интегрированый с расписанием на портале infoclinica.ru</h2>

Изначально выбирается отделение, потом парсятся все доступные специальности и предлагается выбрать направление. 
После выбора направления парсится список врачей, у которых есть активные окошки для записи в ближайшие 30 дней, 
и предлагается выбор врача. Затем парсятся даты и предлогается выбор. Если выбрано направление диагностика, то 
не предоставляется возможность выбора времени, а сразу переходит в состояние FSM и к заполнению контактной 
информации. Если направление НЕ диагностика, то предоставляется возможность выбора свободного времени приема,
после чего также переходит к заполнению формы. После заполнения формы данные о записи сохраняются в бд и 
отправляются оператору в телеграм-чат, а пользователю приходит уведомление о записи. 


Основные настройки вынесены в файл <b>config.py</b>:
<ul>
  <li><b>TOKEN</b> = " " #токен телеграм-бота</li>
  <li><b>operator</b> = " " #ID телеграмма оператора</li>
  <li><b>url_clinic</b> = 'https://NAME.infoclinica.ru' #сайт клиники на портале инфоклиника</li>
  <li><b>DataBase</b> = 'db.sqlite3' #путь к базе данных</li>
  <li><b>log_path</b> = 'log/log.log' #путь для ведения логов.</li>
  <li><b>subject</b> = 'Тема письма'</li>
  <li><b>sender_email</b> = 'admin@example.com' #логин почты</li>
  <li><b>receiver_email</b> = 'admin@example.com' #кому отправлять</li>
  <li><b>password</b> = 'pass' #пароль поты</li>
  <li><b>host_mail</b> = 'smtp.yandex.ru' #адрес почтового сервера</li>
  <li><b>host_port</b> = 465 #порт почтового сервера</li>
 </ul>
