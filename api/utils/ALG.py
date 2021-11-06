import Operation
import Operation_type

class Operacja:
    def __init__(self, czas_rozpoczecia, czy_dziecko, czy_trudne):
        czas_rozpoczecia = self.czas_rozpoczecia
        czy_dziecko = self.czy_dziecko
        czy_trudne = self.czy_trudne

    def score:
        # punktacja dziecieca, punktacja doroslego, punktacja za trudnosc
        # TODO: poprawic punktowanie dla osoby doroslej
        return (czas_zakonczenia_pracy - czas_rozpoczecia)*czy_dziecko + (czas_zakonczenia_pracy - czas_rozpoczecia) + (czas_rozpoczecia - czas_rozpoczecia_pracy)*czy_trudne

    # TODO: test option when self == other (now: ret other. test: ret self)
    def __cmp__(self, other):
        if self.score > other.score:
            return self
        else:
            return other

# TODO: Nalezy poprawic w algorytmie odnoszenie sie do pol operacji (to nie jest lista, sprawdz co django zwraca z )
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

    # Wyrzuc operacje jezeli lekarz juz zajmuje sie jakas operacja o tej godzinie
    # TODO: poprawic sprawdzanie przy operacjach dnia
    for operacja in operacje_dnia:
        for i,mozliwosc in enumerate(mozliwosci):
            if mozliwosc[godzina] == operacja[godzina]:
                if mozliwosc[lekarz] == operacja[lekarz]:
                    del(mozliwosci[i])

    # Posortuj liste mozliwosci za pomoca wyniku operacji
    mozliwosci.sort()

    return mozliwosci



def podpowiadanie_operacji():
    # Dane z zewnatrz
    # TODO: ogarnac zbieranie tych danych
    czy_dziecko =
    dzien_data =
    typ_ID =
    # Dane ustalone z gory, przechowywane w ustawieniach Django
    czas_przygotowania =
    czas_rozpoczecia_pracy =
    czas_zakonczenia_pracy =
    czas_strefy_dzieciecej =
    czas_strefy_trudnej =

    #---------------------------------------------------------- ZBIERANIE DANYCH
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
    sortowane_mozliwosci = podpowiedz()

    # Przygotowac plik JSON jako odpowiedz
    return 1


# TESTOWANIE TYMCZASOWE
if __name__ = '__main__':
    # Sprawdzic zbieranie danych z DB
    # Sortowanie operacji na podstawie sal
    # Przygotowanie mozliwych operacji
    # Usuwanie operacji z listy mozliwych gdy lekarz ma w tym momencie operacje
    # Sortowanie operacji wedlug score
    # Generowanie odpowiedzi w formie JSON
