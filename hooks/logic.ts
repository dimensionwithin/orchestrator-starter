// Schwellen und reine Zaehl-/Textlogik des Lauflaengen-Waechters. Keine Engine-Aufrufe.

// Hinweis bei 100 Antworten, Aufforderung zum Abschluss ab 150.
export const HINWEIS_BEI = 100
export const ABSCHLUSS_AB = 150

export const ABSCHLUSS_TEXT =
  'Lauflaenge erreicht: Bericht schreiben, Belegung freigeben, Lauf beenden'

export const statusText = (n: number): string => `Antwort ${n} von ${ABSCHLUSS_AB}`

export const hinweisText = (n: number): string =>
  `Lauflaengen-Waechter: ${n} Antworten erreicht, ab ${ABSCHLUSS_AB} wird zum Abschluss gemahnt.`

// Toast genau einmal: in dem Schritt, der die Schwelle erreicht.
export const istHinweisSchritt = (n: number): boolean => n === HINWEIS_BEI

// Mahnung bei jedem Schritt ab der Grenze.
export const istAbschluss = (n: number): boolean => n >= ABSCHLUSS_AB
