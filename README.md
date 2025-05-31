## TODO:
## 1. Parametryzacja i konfiguracja analizy społeczności
- Umożliwienie wyboru różnych algorytmów wykrywania społeczności (np. Louvain, Girvan-Newman, Label Propagation).
- Dostosowywanie parametrów algorytmów przez użytkownika (np. graniczna liczba społeczności, poziom modularności).

## 2. Optymalizacja wyświetlania grafu
- Możliwość regulacji wielkości wierzchołków w zależności od wybranej metryki (np. liczba interakcji, stopień w grafie). DONE
- Ograniczenie liczby wierzchołków/połączeń wyświetlanych jednocześnie w celu zwiększenia przejrzystości i wydajności. Ustawienie maksymalnej liczby do takiego poziomu, żeby nie zabijał funkcjonalności strony. DONE
- Wstępne filtrowanie i redukcja danych przy wczytywaniu (np. najaktywniejsze konta, interakcje powyżej progu).
- Optymalizacja czasu wczytywania danych i renderowania grafu.

## 3. Analiza i rozszerzenia grafowe
- Zastosowanie dodatkowych algorytmów analizy grafu, np.:
  - centralności (degree, closeness, betweenness),
  - wykrywanie kluczowych węzłów (influencerów),
  - analiza spójności i struktur lokalnych (np. triady, motywy).

## 4. Organizacja interfejsu
- Oddzielenie widoków:
  - dedykowany widok do eksploracji i porównywania różnych zbiorów danych, DONE
  - oddzielny widok do analizy i wizualizacji grafu konkretnego zbioru. DONE

## 5. Wizualizacja treści i embedding (Dodatkowo)
- Osadzenie tweetów w przestrzeni wektorowej za pomocą metod typu t-SNE lub UMAP.
- Jednorazowe wykonanie embeddingu, zapisanie wyników jako pliku binarnego (np. `.npz`, `.pkl`) w celu przyspieszenia ponownego wczytania.
