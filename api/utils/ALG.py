# TODO: poprawic nazwe importa
import Operation
import Operation_type

class Operacja:
    def __init__(self, czas_rozpoczecia, czy_dziecko, czy_trudne):
        czas_rozpoczecia = self.czas_rozpoczecia
        czy_dziecko = self.czy_dziecko
        czy_trudne = self.czy_trudne

    def __cmp__:
        # TODO: dodac sposob liczenia score
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

    # Mozliwe pozycje dla operacji
    mozliwosci = []

    for operacje_w_jednej_sali in enumerate(operacje_dnia):
        for i,operacja in enumerate(operacje_w_jednej_sali):

            # Sprawdzanie przerw miedzy operacjami
            if i+1 < len(operacje_dnia):
                # Sprawdz przerwe miedzy i-ta operacja a i+1
                przerwa = operacja[rozpoczecie]+czas_trwania - operacje_w_jednej_sali[i+1][rozpoczecie]
                # Sprawdz czy mozna ustawic operacje w tej przerwie
                if przerwa + czas_przygotowania > czas_trwania:
                    # TAK: dodaj operacje do mozliwosci
                    mozliwosci.append(Operacja(czas_rozpoczecia, czy_dziecko, czy_trudne))
                # Nie: kontynuuj prace

    # TODO: Wyrzuc operacje jezeli lekarz juz zajmuje sie jakas operacja o tej godzinie ale w innej sali

    # Posortuj liste mozliwosci za pomoca wyniku operacji
    mozliwosci.sort()

    return mozliwosci



if __name__ = '__main__':
    #Dane z zewnatrz
    # TODO: ogarnac zbieranie tych danych
    czy_dziecko =
    dzien_data =
    typ_ID =
    # Dane ustalone z gory, przechowywane w ustawieniach Django
    czas_przygotowania =
    czas_rozpoczecia_pracy =
    czas_strefy_dzieciecej =
    czas_strefy_trudnej =

    #---------------------------------------------------------- ZBIERANIE DANYCH
    # TODO: upewnic sie ze dziala
    operacje_dnia = Dzien.object.raw("SELECT * FROM myapp_operation WHERE date = $s", [dzien_data])
    typ_operacji = Operation_type.object.get(typ_ID)

    #------------------------------------------------------ PRZYGOTOWANIE DANYCH
    # sortowanie operacji wedlug sal
    lista_salo_operacji = []
    while len(operacje_dnia) > 0:
        temp_list = []
        sala = operacje_dnia[0][]                               #TODO: uzupelnic
        for operacja in operacje_dnia:
            if operacja[] == sala:
                temp_list.append(operacja)
                operacje_dnia.remove(operacja) # Mozliwa kolizja petli z usuwaniem
            # 1. wez nr_sali z pierwszej napotkanej sali
            # 2. operacje o tej samej sali wrzuc do listy oraz wyrzuc je z operacji dnia
            # 3. na koniec wrzuc liste do lista_salo_operacji

    # TODO: foramatowanie czasu
    # NOTE: wydzielic wszystko na oddzielne funkcje zeby latwo sprawdzac bledy
    sortowane_mozliwosci = podpowiedz()
