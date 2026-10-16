import type { Register } from 'claude-code'
import {
  ABSCHLUSS_TEXT,
  hinweisText,
  istAbschluss,
  istHinweisSchritt,
  statusText,
} from './logic'

// Zaehlt je Lauf (= Session; `claude -p` ist eine Session) die Modell-Anfragen der
// Hauptschleife. Subagenten-Schritte tragen eine agentId und zaehlen nicht mit.
// Der Zaehler liegt in der Modulvariable: ein Hot-Reload in einer interaktiven Sitzung
// setzt ihn zurueck; fuer `-p` (laedt immer frisch) ohne Folgen.
export const register: Register = on => {
  let count = 0

  on('session.start', ($, e, next) => {
    count = 0
    return next(e)
  })

  on('session.end', ($, e, next) => {
    count = 0
    $.ui.status(undefined)
    return next(e)
  })

  // turn.step streamt: Generator, der den Strom unveraendert durchreicht.
  on('turn.step', async function* ($, e, next) {
    if (e.agentId === undefined) {
      count += 1
      $.ui.status(statusText(count))
      $.ui.log(`${statusText(count)} (turn ${e.turnId}, index ${e.index})`, { to: 'debug' })
      if (istHinweisSchritt(count)) $.ui.toast(hinweisText(count))
    }
    return yield* next(e)
  })

  // Ab der Grenze haengt der Mod an das Ergebnis jedes Tool-Aufrufs der Hauptschleife
  // einen Hinweis fuer das Modell an. Er verweigert nichts und aendert das Ergebnis nicht.
  on('tool.call', async ($, e, next) => {
    const ran = await next(e)
    if (e.agentId !== undefined || !istAbschluss(count) || ran.deny !== undefined) return ran
    return { ...ran, context: [...(ran.context ?? []), ABSCHLUSS_TEXT] }
  })
}
