# TODO: poprawic nazwe importa
import Dzien

# TODO: wydzielic do oddzielnego pliku
class Operacja:
    def __init__(self, czas_rozpoczecia, czy_dziecko, czy_trudne):

    def score:
        return 1


def podpowiedz(operacje_dnia, lekarz_ID, czy_dziecko, czy_trudne, czas_trwania, czas_przygotowania):
    """
    Zwraca posortowana liste mozliwych operacji wedlug systemu okreslania zdatnosci

    ARGS:
    operacje_dnia - lista list operacji, sortowane wedlug sal
    lekarz_ID - id lekarza w DB
    czy_trudne - wartosc -1/1
    czy_dziecko - wartosc -1/1
    czas_trwania - czas trwania operacji podany w minutch
    czas_przerwy - czas trwania przerwy pooperacyjnej podany w minutch
    """

    #Mozliwe pozycje dla operacji
    mozliwosci = []

    for operacje_w_jednej_sali in enumerate(operacje_dnia):
        for i,operacja in enumerate(operacje_w_jednej_sali):

            # Sprawdzanie przerw miedzy operacjami
            if i+1 < len(operacje_dnia):
                #sprawdz przerwe miedzy i-ta operacja a i+1
                przerwa = operacja[rozpoczecie]+czas_trwania - operacje_w_jednej_sali[i][rozpoczecie]
                #sprawdz czy mozna ustawic operacje w tej przerwie
                if przerwa + czas_przygotowania > czas_trwania:
                    #TAK: dodaj operacje do mozliwosci
                    mozliwosci.append(Operacja(czas_rozpoczecia, czy_dziecko, czy_trudne)) # TODO: sprawdzic konstrukcje
                #Nie: kontynuuj prace

    # TODO: Wyrzuc operacje jezeli lekarz juz zajmuje sie jakas operacja o tej godzinie

    # Posortuj liste mozliwosci za pomoca score operacji
    mozliwosci.sort(key=score()) # TODO: sprawdz czy mozna sortowac metoda

    return mozliwosci



if __name__ = '__main__':
    #Dane z zewnatrz
    # TODO: ogarnac zbieranie tych danych
    czy_dziecko = -1
    dzien_ID = 123
    typ_ID = 123
    # Dane ustalone z gory
    # TODO: nalezy przechowac te dane i pobierac je
    czas_przygotowania = 15
    czas_rozpoczecia_pracy = 480 #czyli 8:00
    czas_strefy_dzieciecej = 120
    czas_strefy_trudnej = 120

    #---------------------------------------------------------- ZBIERANIE DANYCH
    # TODO: FIX MERGE ISSUES
    operacje_dnia = Dzien.object.get(dzien_ID)
    typ_operacji = Typ_operacji.object.get(typ_ID)

    #------------------------------------------------------ PRZYGOTOWANIE DANYCH
    # sortowanie operacji wedlug sal
    lista_salo_operacji = []
    while len(operacje_dnia) > 0:
        for i in operacje_dnia:
            # 1. wez nr_sali z pierwszej napotkanej sali
            # 2. operacje o tej samej sali wrzuc do listy oraz wyrzuc je z operacji dnia
            # 3. na koniec wrzuc liste do lista_salo_operacji

    # TODO: foramatowanie czasu

    sortowane_mozliwosci = podpowiedz()
