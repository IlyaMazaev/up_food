# -*- coding: utf-8 -*-
import os

import pymorphy2  # creating tags based on words morphology
from PIL import Image  # to show pics of recipes

from database_work.data import db_session  # db engine
from database_work.data.products import Product  # orm Recipe class
from database_work.data.recipes import Recipe  # orm Recipe class


def main():
    db_session.global_init("db/recipes_data.db")  # connecting to db

    db_sess = db_session.create_session()

    for el in products_for_recipe_search(input()):
        print(el)

    '''
    print(db_sess.query(Product).filter(Product.tags.like('%' + 'мука' + '%')).first())
    print(db_sess.query(Product).filter(Product.tags.like('%' + 'мука' + '%')).first().get_json_data())
    '''

    add_new_recipe('Домашние беляши',
                   'Вода - 500 г; Масло растительное - 2 ст. ложки;Мука - 500 г;Соль - 1 ч. л.;Сахар - по вкусу (немного);Дрожжи сухие - 1 ч. л.;Мясо (говядина и свинина) - 400-500 г;Лук репчатый - 200-300 г;Перец черный - по вкусу',
                   {'Масло растительное': [1670, 1667],
                    'Мука': [2188, 2190],
                    'Соль': [2349, 2342],
                    'Сахар': [5122, 5124],
                    'Дрожжи сухие': [2284, 2283],
                    'Говядина': [2917, 2924],
                    'Свинина': [2990, 2991],
                    'Лук репчатый': [1267, 1257]},
                   'В ведерко хлебопечки налить теплую воду (500 мл), влить 2 ст. ложки растительного масла, всыпать 500 г муки, 1 ч. л. соли, чуть сахара. Насыпать 1 ч. л. сухих дрожжей в ямку в середине мучной горки. (Если нужно, чтобы тесто получилось в пирожках пышным и воздушным, можно подсыпать немного пекарского порошка в муку.)Поставить ведерко в хлебопечку и запустить ее в режиме "подъем теста без выпекания". Не торопиться закрывать крышку. Если тесто покажется несколько жидковатым, вполне можно добавить еще муки, или воды, если тесто замешивается слишком крутым. Из теста должен образоваться шар эластичной консистенции.\n\tФарш для приготовления беляшей можно приготовить из любого мяса, это дело индивидуального вкуса домашнего кулинара. Мясо желательно пропускать через мясорубку с крупной решеткой, а лук для фарша мелко нарезать. Солить фарш лучше непосредственно перед приготовлением беляшей.\n\tИтак, когда верная помощница хлебопечка возвестила о подошедшем тесте, можно приниматься за жарку беляшей.\nВыложить тесто в глубокую миску. Оторвать от теста небольшой его кусочек, разделить на нужные по размеру части, дать полежать им пару минут. Затем пальчиками сделать в каждом кусочке теста углубление. Не раскатывая скалкой, положить туда начинку, чуть примять и закрепить края, завернув их к середине, оставить небольшое отверстие.\n\tКласть каждый пирожок отверстием вниз в сильно разогретое растительное масло. Переворачивать по мере готовности одной стороны.\n\tЕсли для жарки беляшей использовать керамическую сковороду (с антипригарным покрытием), то беляши не будут "купаться" в излишнем количестве растительного масла.\n\tОсобенно хороши домашние беляши с чашкой горячего бульона в зимнюю стужу. А летом - холодная окрошка вприкуску с беляшами будет сытным и питательным блюдом.\n\tПриятного аппетита!',
                   '2', '1 час', 'Домашняя кухня;Выпечка;Мясо')

    add_new_recipe('Борщ с говядиной',
                   'Говядина - 500 г;Свёкла - 1 шт.;Картофель - 2 шт.;Капуста белокочанная - 200 г;Морковь - 1 шт.;Лук репчатый - 1 шт.;Томатная паста - 1 ст. ложка;Масло растительное - 2 ст. ложки;Уксус - 1 ч. ложка;Лавровый лист - 1 шт.;Перец чёрный горошком - 2-3 шт.;Соль - 2 ч. ложки (по вкусу);Вода - 1,5 л;Зелень укропа и/или петрушки - 3-4 веточки;Сметана - 2 ст. ложки',
                   {'Говядина': [2917, 2924],
                    'Свёкла': [1270, 1272],
                    'Картофель': [1242, 1244],
                    'Капуста белокочанная': [1303, 1429],
                    'Морковь': [1251, 1250],
                    'Лук репчатый': [1267, 1257],
                    'Томатная паста': [4296, 4298],
                    'Масло растительное': [1670, 1667],
                    'Уксус': [4345, 4348],
                    'Лавровый лист': [2039, 2042],
                    'Перец чёрный горошком': [1924, 1933],
                    'Зелень': [1447, 1438],
                    'Сметана': [1089, 1097]},
                   'Говядину нарезать крупными кусками.\nЗалить мясо в кастрюле холодной водой, довести до кипения, снять пену. Варить бульон примерно 1,5 часа на небольшом огне. В конце ваки посолить.\nСвёклу очистить, нарезать соломкой.\nМорковь очистить, натереть на крупной терке.\nЛук очистить, мелко нарезать.\nКапусту нашинковать.\nКартофель очистить, нарезать кубиками.\nНа сковороде разогреть растительное масло. Свёклу, морковь и лук выложить на сковороду и тушить на среднем огне (пассеровать), помешивая, 5-7 минут.\nВ конце добавить уксус и томатную пасту. Перемешать. Готовить овощи ещё 3-4 минуты, помешивая.\nВ кипящий бульон выложить картофель и капусту, варить 10 минут. (Молодую капусту добавлять за 5 минут до окончания приготовления борща.)\nЗатем добавить пассерованные овощи, лавровый лист и перец. Варить борщ с говядиной еще 5-7 минут.\nГотовому борщу дать настояться 10-15 минут. Зелень нарезать.\n Можно разливать борщ по тарелкам, заправлять сметаной и посыпать зеленью.',
                   '4', '1 час', 'Домашняя кухня;Суп')

    add_new_recipe('Блины на молоке: традиционный рецепт',
                   'Молоко - 0,5 л;Яйца - 3 шт.;Масло растительное - 2 ст. ложки;Мука - 250 г;Сахар - 1 ст. ложка;Соль - 1 щепотка;Масло сливочное - 1 ст. ложка',
                   {'Молоко': [2, 16],
                    'Яйца': [925, 924],
                    'Масло растительное': [1670, 1667],
                    'Мука': [2188, 2190],
                    'Сахар': [5122, 5124],
                    'Соль': [2349, 2342],
                    'Масло сливочное': [943, 955]},
                   'Смешайте яйца, соль, сахар и размешайте миксером. Введите муку и влейте молоко. Взбейте блинное тесто, чтобы добиться однородной консистенции.\nСледом отправьте в тесто растительное масло, чтобы блины в момент жарки легко переворачивались и не пригорали.\nРазогрейте сковородку и смажьте маслом.\nНалейте в центр сковородки небольшую порцию теста. Сразу же вращайте сковородку по кругу, чтобы тесто равномерно распределилось по всей поверхности.\nЖарим блины на среднем огне с обеих сторон до зарумянивания. Блины очень тонкие, поэтому переворачивайте их аккуратно с помощью лопатки. После того, как блин будет готов, снимите со сковородки и смажьте сливочным маслом, чтобы края не были сухими, а блины получились нежными.\nБлины на молоке можно подавать с вареньем, джемом или сгущенкой.\n Приятного аппетита!',
                   '3', '30 минут', 'Домашняя кухня;Выпечка')

    add_new_recipe('Куриный суп с вермишелью',
                   'Филе куриное - 2 шт. (500 г);Картофель - 2-3 шт.;Морковь - 1 шт.;Лук репчатый - 1 шт.;Вермишель - 100 г;Зелень петрушки (для подачи) - по вкусу;Лист лавровый - 2 шт.;Перец черный молотый - 2 щепотки (по вкусу);Соль - 3 щепотки (по вкусу);Масло растительное - 2 ст. л.;Вода - 2 л',
                   {'Филе куриное': [2580, 2585],
                    'Картофель': [1243, 1249],
                    'Морковь': [1251, 1252],
                    'Лук репчатый': [1267, 1257],
                    'Вермишель': [1548, 1551],
                    'Зелень петрушки': [1447, 1441],
                    'Лавровый лист': [2039, 2042],
                    'Перец черный молотый': [1932, 1919],
                    'Масло растительное': [1670, 1667]},
                   'Куриное филе вымойте, обсушите, срежьте с филе пленки и нарежьте его крупно.\nВыложите курицу в кастрюлю, залейте холодной водой, добавьте лавровые листья. Доведите до кипения и снимите пену. Варите куриное филе 15 минут, после чего выложите кусочки филе на тарелку.\nМорковь натрите на крупной терке.\nЛук нарежьте мелкими кубиками.\nРазогрейте на сковороде растительное масло и обжарьте на умеренном огне (спассеруйте) нарезанный лук примерно 2-3 минуты, до мягкости.\nДобавьте к луку натертую морковь, перемешайте и обжаривайте лук и морковь еще 2 минуты.\nКартофель нарежьте средними кубиками или брусочками.\nКуриное филе нарежьте кусочками.\nДобавьте в кастрюлю с бульоном картофель и варите примерно 10 минут.\nПосле этого добавьте приготовленную зажарку (пассеровку).\nВ суп с овощами добавьте куриное филе.\nВсыпьте в суп с курицей вермишель, добавьте соль и молотый перец по вкусу. Перемешайте.Варите куриный суп с вермишелью 5-7 минут. (При желании можно добавить в суп измельченную зелень петрушки.)\nГотовому куриному супу дайте настояться несколько минут. Затем разлейте суп с вермишелью по тарелкам, посыпьте измельчённой свежей зеленью и подавайте к столу.\nПриятного аппетита!',
                   '4', '1 час', 'Домашняя кухня;Суп')

    add_new_recipe('Пирог с яблоками и карамелью',
                   'Яблоки твердые, кислых сортов - 2 шт.;Сок лимона;Яйца - 4 шт.;Масло сливочное, растопленное - 225 г;Мука - 3,25 стакана;Разрыхлитель - 3 ч. ложки;Сахар светло-коричневый - 2 стакана;Сахар - 1 ст. ложка;Соль - щепотка',
                   {'Яблоки': [1238, 1337],
                    'Сок лимона': [2167, 1372],
                    'Яйца': [925, 924],
                    'Масло сливочное': [943, 955],
                    'Мука': [2188, 2190],
                    'Разрыхлитель': [2289, 2291],
                    'Сахар светло-коричневый': [5114],
                    'Сахар': [5122, 5124]},
                   'Разогреть духовку до 180 градусов. Застелить пергаментом дно противня размером 23х33 см.\nЯблоки очистить от семян и кожуры, нарезать тонкими ломтиками. Яблочные дольки полить лимонным соком, перемешать, чтобы не потемнели.\nМуку смешать с разрыхлителем, добавить коричневый сахар. Вбить яйца, добавить растопленное сливочное масло и миксером перемешать тесто до однородности.\nВыложить тесто в подготовленную форму, разровнять верх.\nСверху выложить дольки яблок в три или четыре ряда. Посыпать сахаром.\nВыпекать пирог с яблоками около 45 минут, чтобы он стал плотным на ощупь.\nПока печется пирог, приготовить карамельный соус. Для этого смешать масло и сахар в соуснике на среднем огне. Добавить лимонный сок и щепотку соли, перемешивать и охладить.\nПолить яблочный пирог карамелью, пока он еще в форме, аккуратно распределяя соус кисточкой по поверхности. Пирог с яблоками и карамелью подавать теплым.',
                   '2', '2 часа', 'Выпечка;Десерт')

    add_new_recipe('Котлеты из мяса индейки',
                   'Мясо индейки - 600 г;Хлеб белый - 1-2 ломтя;Молоко - 0,5 стакана;Яйца - 1 шт.;Масло сливочное - 60 г;Сухари панировочные - 0,5 стакана ;Пряности (перец, карри, куркума, чеснок) - по вкусу;Соль - 1 ст. ложка (по вкусу);Масло растительное (или жир) для жарки - 40 г',
                   {'Мясо индейки': [2579, 2587],
                    'Хлеб белый': [2376, 2428],
                    'Молоко': [2, 16],
                    'Яйца': [925, 924],
                    'Масло сливочное': [943, 955],
                    'Сухари панировочные': [2071, 2068],
                    'Масло растительное': [1670, 1667]},
                   '\nВключить духовку.\nБелый хлеб замочить в молоке. Отжать.\nМясо индейки разрезать на части.\nМясо вместе со смоченным в молоке и отжатым белым хлебом пропустить через мясорубку.\nЗатем добавить пряности, яйцо и 40 г размягченного сливочного масла.\nВсе тщательно перемешать.\nМокрыми руками сформовать небольшие котлеты, запанировать в сухарях.\nРазогреть сковороду, добавить растительное масло (или жир). В горячее масло выложить подготовленные котлеты.\nКотлеты обжарить на разогретом масле (или жире) на среднем огне с обеих сторон до золотистости (1-2 минуты с каждой стороны).\nЗатем поставить их на 10-15 минут в не горячую духовку (160 градусов).\nКотлеты из мяса индейки готовы.\nПриятного аппетита!',
                   '4', '45 минут', 'Домашняя кухня;Мясо;Индейка')

    add_new_recipe('Торт без выпечки «Домик»',
                   'Творог свежий, жирный — 400-500 г;Масло сливочное — 150-200 г;Сахар (если творог несладкий) — по вкусу;Ванильный сахар — по вкусу;Мармелад разноцветный — 300-400 г (или по вкусу);Лимонная цедра, тертая на мелкой терке — по вкусу;Какао — 2-3 ст. л.;Печенье квадратной формы — 30 шт.',
                   {'Творог': [506, 505],
                    'Масло сливочное': [943, 955],
                    'Сахар': [5122, 5124],
                    'Ванильный сахар': [2248, 2255],
                    'Мармелад разноцветный': [5811, 5844],
                    'Лимонная цедра': [2259],
                    'Какао': [5137, 2266],
                    'Печенье': []},
                   'Хорошо взбейте размягченное сливочное масло с сахаром (добавляя сахар, не забывайте про сладость мармелада и печенья) и ванильным сахаром.\n Смешайте масло с творогом и взбейте до однородности.\n Нарежьте мармелад мелкими кусочками.\n Лимонную цедру и мармелад добавьте в творожную массу и хорошо перемешайте.\n Разделите пополам. В одну часть вмешайте какао.\n Выложите печенье на пергамент (или на фольгу) в виде прямоугольника 3х5.\n Равномерно выложите на слой печенья творожную массу с какао. Покройте вторым слоем печенья, а сверху выложите белую творожную массу.\n Аккуратно приподнимая две продольные стороны прямоугольника и удерживая их по всей длине, сложите печенье так, чтобы получился длинный треугольный тортик. Внутри окажется белая начинка.\n Посыпьте тортик раскрошенным печеньем, кокосовой стружкой или какао (украсьте по вашему желанию).\n Оставьте на какое-то время при комнатной температуре, а затем поместите в холодильник до следующего дня.\n Вкуснее кушать тортик даже через два дня, когда печенье хорошо пропитается. Готовый тортик разрежьте в охлажденном виде на треугольные пирожные.\n Приятного чаепития!',
                   '4', '30 минут', 'Десерт')

    add_new_recipe('Куриное филе со сладким перцем и грибами',
                   'Бекон, разрезанный вдоль на две части – 1 полоска;Куриное филе – 2 шт. (по 120 г);Салатная заправка «Ранчо» или майонез – 2 ст. л.;Грибы свежие, нарезанные – 3 ст. л.;Перец сладкий, красный – 3 ст. л.;Лук зеленый, нарезанный – 3 ст. л.;Мука кукурузная – 2 ч. л.;Молоко концентрированное – 6 ст. л.',
                   {'Бекон': [2952],
                    'Филе куриное': [2580, 2585],
                    'Майонез': [4204, 4207],
                    'Грибы свежие': [5336, 5344],
                    'Перец сладкий': [1311, 1312],
                    'Лук зеленый': [],
                    'Мука кукурузная': [2216],
                    'Молоко концентрированное': [1182]},
                   'Слегка обжарьте бекон на антипригарной сковороде до мягкости, но не пережаривая. Выложите на бумажное полотенце.\n Отбейте куриные грудки до толщины 0,7 см. Смажьте салатной заправкой «Ранчо» (этот соус можно заменить майонезом, или сделать заправку «Ранчо» самостоятельно, смешав ¾ чашки кефира, 2-3 ст. л. лимонного сока, измельченную петрушку или кинзу, перец, соль).\n На смазанное соусом мясо выложите грибы, нарезанный сладкий перец и зеленый лук. Сверните рулетом и оберните полоской бекона. Если необходимо, закрепите зубочисткой.\n На смазанном масле противне запекайте куриное филе с начинкой в духовке при температуре 180 градусов в течение 25-30 минут.\n Процедите образовавшийся при запекании куриных рулетов сок. Добавьте к нему кукурузную муку, молоко и доведите в кастрюльке до кипения. Помешивая, готовьте соус 1 минуту до загустения. Подайте куриное филе со сладким перцем и грибами под соусом.',
                   '4', '1 час 30 минут', 'Мясо;Курица')

    add_new_recipe('Жареная цветная капуста в кляре',
                   'Цветная капуста - 600 г;Масло сливочное (или растительное) - 3 ст. ложки;Яйца - 1-2 шт.;Сметана - 50 г;Мука - 2-3 ст. ложки;Соль - по вкусу;Перец - по вкусу',
                   {'Цветная капуста': [1305, 1308],
                    'Масло сливочное': [943, 955],
                    'Яйца': [925, 924],
                    'Сметана': [1089, 1097],
                    'Мука': [2188, 2190]},
                   'Цветную капусту промыть,разобрать на соцветия.\nВскипятить воду, посолить. Поместить капусту в кипяток. Варить на небольшом огне до мягкости (7-10 минут).\nГотовую капусту откинуть на дуршлаг.\nСделать кляр. Для этого в миску вбить яйцо, добавить сметану.\nПосолить, поперчить, добавить муку. Взбить кляр. Кляр по густоте получится как густая сметана.\nСоцветия капусты обмакнуть в кляр.\nРазогреть сковороду, добавить масло. В горячее масло выложить капусту.\nЖарить на среднем огне, периодически помешивая, 2-3 минуты (до золотистости).\nЖареная цветная капуста в кляре готова.\nПриятного аппетита!',
                   '3', '45 минут', 'Закуски;Гарниры')

    '''
    add_new_recipe('Сырные шарики с чесноком и петрушкой',
                   'Мука – 1 ¾ стакана;Разрыхлитель – 1 ст. л. и 2 ч. л.;Сахар – 2.5 ч. л.;Соль – 0.25 ч. л.;Маргарин размягченный – 3 ст. л.;Масло сливочное – 80 г (холодное, нарезанное кусочками по 1 см) + 3 ст. л.;Сыр «Чеддер» тертый – 170 г;Молоко – 0.75 стакана;Масло сливочное – 3 ст. л.;Чеснок – 1 зубчик;Зелень петрушки измельченная – 1 ч. л.',
                   {'Мука': [1, 2, 3],
                    'Разрыхлитель': [],
                    'Сахар': [],
                    'Маргарин размягченный': [],
                    'Масло сливочное': [],
                    'Сыр «Чеддер» тертый': [],
                    'Молоко': [],
                    'Чеснок': [],
                    'Зелень петрушки': []},
                   'Разместите решетку в верхней трети духовки и разогрейте духовку до 220 градусов. Слегка смажьте большой противень.\n С помощью кухонного комбайна или вручную приготовьте тесто. Смешайте муку, разрыхлитель, сахар и соль. Добавьте маргарин. Перемешайте до однородности. Добавьте масло. Перемешайте так, чтобы кусочки масла были размером с горошины. Вмешайте сыр. Влейте молоко. Слегка перемешайте. Замесите тесто, но не месите его долго, иначе сырные шарики не получатся рассыпчатыми.\n Выкладывайте тесто порциями (по ¼ стакана) на противень, на расстоянии 5 см. Выпекайте сырные шарики около 20 минут до золотистого цвета.\n Сделайте чесночное масло. Растопите сливочное масло (3 ст. л.) вместе с раздавленным зубком чеснока на среднем огне. Готовьте 1 минуту. Снимите с огня и вмешайте петрушку. Смажьте сырные шарики приготовленным маслом и подавайте теплыми.\n Приятного аппетита!',
                   '2', '1 час', 'Закуски')

    add_new_recipe('Закуска «жареные помидоры»',
                   'Помидоры - 2 шт.;Сыр «Эмменталь» тертый - 100 г;Сахар - 1 ст. ложка;Масло оливковое - 1 ст. ложка;Соль;Орегано',
                   {'Помидоры': [1, 2, 3],
                    'Сыр «Эмменталь»': [],
                    'Сахар': [],
                    'Масло оливковое': [],
                    'Орегано': []},
                   'Разогрейте духовку до 220 градусов. Нарежьте помидоры толстыми кружочками.\nРешетку гриля застелите пергаментной бумагой. На бумагу выложите кружочки помидоров.\nПосыпьте сахаром, солью. Равномерно распределите тертый сыр. Сверху посыпьте орегано.\nПолейте оливковым маслом.\nПоставьте в духовку на 7 минут.\nЖареные помидоры с сыром готовы.\n Приятного аппетита!',
                   '2', '45 минут', 'Закуски')

    

    add_new_recipe('Пастила',
                   'Желатин - 30 г;Вода - 1 ст.;Сахар - 420 г;Патока или сироп - по вкусу;Соль - 0.25 ч.л.;Яичный белок - 2 шт.;Ванильный сахар - 1 уп.;Сахарная пудра со вкусом ванили - 0.5 уп.;Крахмал - 25 г',
                   {'Желатин': [1, 2, 3],
                    'Сахар': [],
                    'Патока или сироп': [],
                    'Яйца для яичного белка': [],
                    'Ванильный сахар': [],
                    'Сахарная пудра со вкусом ванили': [],
                    'Крахмал': []},
                   'Желатин залить ½ ст. горячей воды и мешать до полного растворения.\n На огонь поставить кастрюлю с сахаром, сиропом, солью и половиной стакана воды. Помешивая, варить на среднем огне около 7 минут.\n Как только сахар расплавится, выключить огонь и добавить желатин. Остудить смесь до комнатной температуры.\n Взбить белки в глубокой посуде, влить туда всю жидкость из кастрюли и взбивать миксером на большой скорости. Когда белки с желатиновой смесью поднимутся, добавить туда ванильный сахар и продолжать взбивать до максимально густой массы.\n Затем смешать крахмал и сахарную пудру. Взять застеленный бумагой для выпекания и смазанный маслом противень и присыпать его смесью из крахмала и сахарной пудры.\n Вылить массу на противень и равномерно распределить ее по всей поверхности. Массу присыпать смесью из крахмала и сахарной пудры и, ничем не накрывая и не убирая в холодильник, оставить пастилу настояться минимум на 3-4 часа.\n Из готовой пастилы формами для печенья или острым ножом сделать нужные вам формы.',
                   '2', '1 час', 'Десерты')
    '''
    '''
    add_new_recipe('', '', '')
    add_new_recipe('', '', '')
    add_new_recipe('', '', '')
    '''
    '''
    add_new_recipe('Пастила3',
                   'Желатин - 30 г;Вода - 1 ст.;Сахар - 420 г;Патока или сироп - по вкусу;Соль - 0.25 ч.л.;Яичный белок - 2 шт.;Ванильный сахар - 1 уп.;Сахарная пудра со вкусом ванили - 0.5 уп.;Крахмал - 25 г',
                   {'Желатин': [10, 20], 'Сахар': [2, 4]},
                   'Желатин залить ½ ст. горячей воды и мешать до полного растворения.\n На огонь поставить кастрюлю с сахаром, сиропом, солью и половиной стакана воды. Помешивая, варить на среднем огне около 7 минут.\n Как только сахар расплавится, выключить огонь и добавить желатин. Остудить смесь до комнатной температуры.\n Взбить белки в глубокой посуде, влить туда всю жидкость из кастрюли и взбивать миксером на большой скорости. Когда белки с желатиновой смесью поднимутся, добавить туда ванильный сахар и продолжать взбивать до максимально густой массы.\n Затем смешать крахмал и сахарную пудру. Взять застеленный бумагой для выпекания и смазанный маслом противень и присыпать его смесью из крахмала и сахарной пудры.\n Вылить массу на противень и равномерно распределить ее по всей поверхности. Массу присыпать смесью из крахмала и сахарной пудры и, ничем не накрывая и не убирая в холодильник, оставить пастилу настояться минимум на 3-4 часа.\n Из готовой пастилы формами для печенья или острым ножом сделать нужные вам формы.',
                   '',
                   '',
                   '')
    '''
    # print(get_products_bonded_with_recipe(db_sess.query(Recipe).filter(Recipe.name.like('Пастила3')).first()))

    product_prices_sum = 0  # stores sum of ingredients prices
    for found_recipe in recipe_tags_search(input()):  # for all matching recipes
        print(found_recipe.ingredients)  # prints ingredients
        for ingredient in found_recipe.ingredients.split(';'):  # iterating product ingredients
            print(ingredient.split(' - ')[0])
            products_found = products_for_recipe_search(ingredient.split(' - ')[0])  # getting list of matching products
            try:
                product_prices_sum += int(
                    products_found[0].price)  # if found adds price of first element to sum variable
            except IndexError:
                pass  # of sequence is empty does nothing
    print(f'Итого: {product_prices_sum}')  # printing sum of found products


def get_all_word_forms(word):
    """input: a word ex:'makaroni'
        returns list of word's forms ex: ['makaronov', 'makarons']"""

    morph = pymorphy2.MorphAnalyzer()
    # getting an infinitive(normal) form of the word
    word_parse = morph.parse(word)[0]  # taking the first parse of the word
    normal_form_word = word_parse.normal_form

    # and creating a set containing only this normal form
    all_forms_set = {str(normal_form_word)}

    # source: https://github.com/kmike/pymorphy2/issues/74
    parseList = morph.parse(word)  # list of all possible parses
    for parse in parseList:
        lexeme = parse.lexeme
        for form in lexeme:
            all_forms_set.add(str(form.word))

    # print(all_forms_set)
    return list(all_forms_set)


def create_tags_for_line(line):
    """creating tags for line of words
    can be used with any type of sentences, names, and such things
    returns line of tags looking like this: 'line;tag1;tag2;tag3'
     tags in this case are the words used in line and their grammatical forms"""
    # replaces some symbols
    line = line.replace("'", '')
    line = line.replace('"', '')
    line = line.replace('_', ' ')
    line = line.replace('_', ' ')
    line = line.replace('«', '')
    line = line.replace('»', '')
    tags = ''

    for word in line.split():  # creating tags for each word
        all_word_forms = get_all_word_forms(word.lower())
        tags += ';'.join(all_word_forms)  # adding word's tags to a single tags line

    return line.lower() + ';' + ';'.join(line.split()).lower() + tags.lower()


def add_new_recipe(name, ingredients, bonded_ingredients, how_to_cook, portions, time, types, photo_address=''):
    """adds new recipe to the db
    needs recipe name, ingredients in format: 'ingr1;ingr2;ingr3'
    tags are being created using create_tags_for_line(name)

    format of bonded_ingredients dict:
    {ingredient name: [matching product ids in db]}
    """
    db_sess = db_session.create_session()
    # if there are a recipe with the name like that
    if db_sess.query(Recipe).filter(Recipe.name == name).first():
        print(f'this recipe already exists({name})')

    else:
        # creating Recipe class object
        recipe = Recipe(name=name,
                        ingredients=ingredients,
                        how_to_cook=how_to_cook,
                        tags=create_tags_for_line(name),
                        portions=portions,
                        time=time,
                        types=types,
                        bonded_ingredients=bonded_ingredients)
        recipe.set_photo_address(photo_address)
        db_sess.add(recipe)
        db_sess.commit()


def add_new_product(name, store, price, type, photo_address=''):
    """adds new product to the db
        needs product name, store and price
        tags are being created using create_tags_for_line(name)
        """
    db_sess = db_session.create_session()
    # if there are a product with the name like that
    if db_sess.query(Product).filter(Product.name == name).first():
        print(f'this product already exists({name})')

    else:
        # creating Recipe class object
        product = Product(name=name,
                          store=store,
                          price=price,
                          type=type,
                          tags=create_tags_for_line(name))
        product.set_photo_address(photo_address)
        db_sess.add(product)
        db_sess.commit()


def recipe_tags_search(search_input):
    """input: searching request
    output: prints found recipes and opens photos
    returns a list of found Recipe objects """

    recipes_found = list()  # list which contains all found recipes
    for word in search_input.split():  # each word is an separated key
        db_sess = db_session.create_session()
        # searches for recipes where tags contain word
        search_query = db_sess.query(Recipe).filter(Recipe.tags.like('%' + word.lower() + '%')).all()
        print(search_query)

        for found_recipe in search_query:  # found recipes for word
            recipes_found.append(found_recipe)
            # printing data
            print('-' * 1000)
            print(found_recipe)
            print(found_recipe.how_to_cook)
            if os.path.isfile(found_recipe.photo_address):  # showing pic if exists
                with Image.open(found_recipe.photo_address) as img:
                    img.show()
            print('-' * 1000)
    # returns a list of found Recipe objects
    return recipes_found


def products_for_recipe_search(search_input):
    """
    input: searching request
    output: prints found products
    returns a list of found Product with matching name"""

    products_found = list()  # list which contains all found recipes
    search_query = []
    for word in list(map(lambda x: x.lower(), search_input.split())):  # each word is an separated search key
        if word not in ['и', 'с', 'из', 'для']:  # filtering prepositions
            db_sess = db_session.create_session()


                # if search_query was empty creates it with search by first word from request
            search_query = db_sess.query(Product).filter(Product.tags.ilike('%' + word.lower() + '%')).all()

            '''
            # filters the list and leaves only products which names contain the word
            
            print(list(filter(lambda x: word.lower() in list(map(lambda x: x.lower(), x.name.split())), search_query)))
            search_query = list(filter(lambda x: word.lower() in list(map(lambda x: x.lower(), x.name.split())), search_query))
            '''

            for found_product in search_query:  # found products for word
                products_found.append(found_product)
    # returns a list of found Recipe objects
    print(products_found)
    return products_found


def get_products_bonded_with_recipe(recipe):
    """returns dict with Product objects bonded with recipe
    return format
    {ingredient name: [Product, Product]}"""
    db_sess = db_session.create_session()

    bonded_products = dict()
    for recipe_name, product_ids in recipe.bonded_ingredients.items():
        bonded_products[recipe_name] = []
        for product_id in product_ids:
            bonded_products[recipe_name].append(db_sess.query(Product).get(product_id))

    print(bonded_products)
    return bonded_products


if __name__ == '__main__':
    main()
