from faker import Faker
from random import randint, randrange, choice
import uuid
import json
import sqlite3

MATERIE = ['matematica', 'italiano', 'latino', 'inglese', 'python', 'storia', 'geografia', 'educazione_fisica', 'educazione_civica', 'storia_dell_arte']

def anagrafica_studenti():
    Faker.seed(0)
    fake = Faker('it_IT')

    totaleStudenti = 10000
    maschi = randint(4500, 5500)
    femmine = totaleStudenti - maschi

    school_mails = list()
    personale_mails = list()
    uuids = list()
    Studenti = list()
    print(f'Maschi: {maschi}\nFemmine: {femmine}')

    for j in range(maschi):
        if j % 100 == 0: print(j)
        temp = dict()
        temp['nome'] = fake.first_name_male()
        temp['cognome'] = fake.last_name()
        anno = randint(2000,2004)
        mese = randint(1, 12)
        giorno = randint(1, 28) if mese in [11, 4,6, 9, 2] else randint(1, 31)
        temp['data_di_nascita'] = f"{anno}-{mese}-{giorno}"
        temp['citta_nascita'] = fake.city()
        temp['domicilio'] = fake.address()
        temp['telefono'] = fake.phone_number()
        temp['contatto_emergenza_telefono'] = fake.phone_number()
        temp['contatto_emergenza_nome'] = fake.name()
        while True:
            matricola = str(uuid.uuid4())
            if matricola not in uuids:
                temp['matricola'] = matricola
                uuids.append(matricola)
                break

        while True:
            mail_personale = fake.ascii_free_email()
            if mail_personale not in personale_mails:
                temp['mail_personale'] = mail_personale
                personale_mails.append(mail_personale)
                break

        i = 1
        while True:
            mail_scuola = f"{temp['cognome']}.{temp['nome']}@liceoleonardodavinci."
            if mail_scuola not in school_mails:
                temp['mail_scuola'] = mail_scuola
                school_mails.append(mail_scuola)
                break
            else:
                mail_scuola = f"{temp['cognome']}.{temp['nome']}_{i}@liceoleonardodavinci."
                if mail_scuola not in school_mails:
                    temp['mail_scuola'] = mail_scuola
                    school_mails.append(mail_scuola)
                    break
                else:
                    i += 1

        Studenti.append(temp)

    for j in range(femmine):
        if j % 100 == 0: print(j)
        temp = dict()
        temp['nome'] = fake.first_name_female()
        temp['cognome'] = fake.last_name()
        anno = randint(2000,2004)
        mese = randint(1, 12)
        giorno = randint(1, 28) if mese in [11, 4,6, 9, 2] else randint(1, 31)
        temp['data_di_nascita'] = f"{anno}-{mese}-{giorno}"
        temp['citta_nascita'] = fake.city()
        temp['domicilio'] = fake.address()
        temp['telefono'] = fake.phone_number()
        temp['contatto_emergenza_telefono'] = fake.phone_number()
        temp['contatto_emergenza_nome'] = fake.name()

        while True:
            matricola = str(uuid.uuid4())
            if matricola not in uuids:
                temp['matricola'] = matricola
                uuids.append(matricola)
                break

        while True:
            mail_personale = fake.ascii_free_email()
            if mail_personale not in personale_mails:
                temp['mail_personale'] = mail_personale
                personale_mails.append(mail_personale)
                break

        i = 1
        while True:
            mail_scuola = f"{temp['cognome']}.{temp['nome']}@liceoleonardodavinci."
            if mail_scuola not in school_mails:
                temp['mail_scuola'] = mail_scuola
                school_mails.append(mail_scuola)
                break
            else:
                mail_scuola = f"{temp['cognome']}.{temp['nome']}_{i}@liceoleonardodavinci."
                if mail_scuola not in school_mails:
                    temp['mail_scuola'] = mail_scuola
                    school_mails.append(mail_scuola)
                    break
                else:
                    i += 1

        Studenti.append(temp)

    with open('anagrafica.json', 'w') as outJson:
        outJson.write(json.dumps(Studenti))

def rettifica():
    Studenti = json.loads(open('anagrafica.json', 'r').read())
    therealstudenti = dict()
    for studente in Studenti:
        therealstudenti[studente['matricola']] = {"nome" : studente['nome'],
                                                  "cognome" : studente['cognome'],
                                                  "data_di_nascita" : studente['data_di_nascita'],
                                                  "citta_nascita" : studente['citta_nascita'],
                                                  "domicilio" : studente['domicilio'],
                                                  "telefono" : studente['telefono'],
                                                  "contatto_emergenza_telefono" : studente['contatto_emergenza_telefono'],
                                                  "contatto_emergenza_nome" : studente['contatto_emergenza_nome'],
                                                  "mail_personale" : studente['mail_personale'],
                                                  "mail_scuola" : studente['mail_scuola']}
    open('anagrafica.json', 'w').write(json.dumps(therealstudenti))

def registro_elettronico():
    print('registro_elettronico chiamata')
    Studenti = json.loads(open('anagrafica.json', 'r').read())
    registro_elettronico = dict()
    Z = 0
    for k, v in Studenti.items():
        if Z % 100 == 0: print(Z)

        registro_elettronico[k]= dict()

        registro_elettronico[k]['anno'] = int(v['data_di_nascita'].split('-')[0]) - 1999
        for i in range(1,6):
            registro_elettronico[k][f'crediti_anno_{i}'] = 0

        for anno in range(1, registro_elettronico[k]['anno']):
            print(f'{anno}')
            registro_elettronico[k][f'crediti_anno_{anno}'] = randint(0, 5)

        for materia in MATERIE:
            registro_elettronico[k][materia] = randint(5,10)
        
        registro_elettronico[k]['assenze'] = randint(5, 35)

        # richiami disciplinari
        registro_elettronico[k]['richiami_disciplinari'] = 1 if randint(0,1000) == 298 else 0

        registro_elettronico[k]['media'] = str(sum([registro_elettronico[k][materia] for materia in MATERIE]) / len(MATERIE))

        Z += 1

    open('registro_elettronico.json', 'w').write(json.dumps(registro_elettronico, indent=2))

def sqlizziamo_Anagrafica():
    Anagrafica = json.loads(open('anagrafica.json', 'r').read())
    DB = sqlite3.connect('db.sqlite')
    cur = DB.cursor()
    TABLE_NAMES = "('matricola', 'nome', 'cognome', 'data_di_nascita', 'citta_nascita', 'domicilio', 'telefono', 'contatto_emergenza_telefono', 'contatto_emergenza_nome', 'mail_personale', 'mail_scuola')"
    VALUES = ""
    for k, v in Anagrafica.items():
        #VALUES += f"('{k}', '{v['nome']}', '{v['cognome']}', '{v['data_di_nascita']}', '{v['citta_nascita']}', '{v['domicilio']}', '{v['telefono']}', '{v['contatto_emergenza_telefono']}', '{v['contatto_emergenza_nome']}', '{v['mail_personale']}', '{v['mail_scuola']}'), "
        cur.execute(f"INSERT INTO anagrafica {TABLE_NAMES} VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                   (k, v['nome'], v['cognome'], v['data_di_nascita'], v['citta_nascita'], v['domicilio'], v['telefono'], v['contatto_emergenza_telefono'], v['contatto_emergenza_nome'], v['mail_personale'], v['mail_scuola'])
                   )


    DB.commit()
    DB.close()


def sqlizziamo_registro():
    Registro_Elettronico = json.loads(open('registro_elettronico.json', 'r').read())
    DB = sqlite3.connect('db.sqlite')
    cur = DB.cursor()
    TABLE_NAMES = "('matricola', 'anno', 'crediti_anno_1', 'crediti_anno_2', 'crediti_anno_3', 'crediti_anno_4', 'crediti_anno_5', 'assenze', 'richiami_disciplinari', 'media')"
    VALUES = ""
    for k, v in Registro_Elettronico.items():
        cur.execute(f"INSERT INTO registro_elettronico {TABLE_NAMES} VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                   (k, v['anno'], v['crediti_anno_1'], v['crediti_anno_2'], v['crediti_anno_3'], v['crediti_anno_4'], v['crediti_anno_5'], v['assenze'], v['richiami_disciplinari'], v['media'], v['matematica'], v['italiano'], v['latino'], v['inglese'], v['python'], v['storia'], v['geografia'], v['educazione_fisica'], v['educazione_civica'], v['storia_dell_arte'])
                   )


    DB.commit()
    DB.close()


if __name__ == "__main__":
    anagrafica_studenti()
    rettifica()
    registro_elettronico()
    sqlizziamo_Anagrafica()
    sqlizziamo_registro()
