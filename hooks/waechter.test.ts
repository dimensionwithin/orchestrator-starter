import { expect, test } from 'claude-code/testing'
import {
  ABSCHLUSS_AB,
  ABSCHLUSS_TEXT,
  HINWEIS_BEI,
  istAbschluss,
  istHinweisSchritt,
  statusText,
} from './logic'

// --- Schwellen- und Textlogik, rein ---

test('Schwellen sind 100 und 150', () => {
  expect(HINWEIS_BEI).toBe(100)
  expect(ABSCHLUSS_AB).toBe(150)
})

test('Statuszeile heisst "Antwort <n> von 150"', () => {
  expect(statusText(7)).toBe('Antwort 7 von 150')
})

test('Hinweis-Schritt trifft nur genau Antwort 100', () => {
  expect(istHinweisSchritt(99)).toBe(false)
  expect(istHinweisSchritt(100)).toBe(true)
  expect(istHinweisSchritt(101)).toBe(false)
})

test('Abschluss-Mahnung erst ab Antwort 150', () => {
  expect(istAbschluss(149)).toBe(false)
  expect(istAbschluss(150)).toBe(true)
  expect(istAbschluss(151)).toBe(true)
})

// --- durch die echte Schicht: Engine-Hooks mit dem Mod darueber ---

const stepInput = (index: number) => ({
  turnId: 't1',
  index,
  model: 'test-modell',
  messageCount: index * 2 + 1,
})

test('Engine: zaehlt Schritte, zeigt Status, Toast bei 100, Hinweis ab 150, verbietet nichts', async ($, on) => {
  const statuses: (string | undefined)[] = []
  const toasts: string[] = []

  on('ui.status', (_$, e) => {
    statuses.push(e.text)
    return null as never
  })
  on('ui.toast', (_$, e) => {
    toasts.push(e.text)
    return null as never
  })
  // Die Engine unter dem Mod: ein Schritt ohne Antwort, ein Tool-Aufruf ohne Wirkung.
  on('turn.step', async function* (_$, e) {
    return { turnId: e.turnId, index: e.index, answer: '', toolUses: [], stopReason: null, usage: null }
  })
  on('tool.call', () => ({ result: 'ok', text: 'ok' }) as never)

  const step = async (index: number) => {
    const stream = $.turn.step(stepInput(index))
    for await (const _chunk of stream) {
      // nichts zu lesen, der Strom ist leer
    }
    await stream.result
  }
  const toolCall = () => $.tool.call({ tool: 'Bash', command: 'echo hi' } as never) as Promise<{
    deny?: string
    context?: readonly string[]
  }>

  // Vor der Grenze: kein Hinweis, nichts verboten.
  await step(0)
  expect(statuses[statuses.length - 1]).toBe('Antwort 1 von 150')
  const early = await toolCall()
  expect(early.deny).toBeUndefined()
  expect(early.context).toBeUndefined()

  // Bis Antwort 100: genau ein Toast.
  for (let i = 1; i < 100; i++) await step(i)
  expect(statuses[statuses.length - 1]).toBe('Antwort 100 von 150')
  expect(toasts.length).toBe(1)

  // Bis Antwort 149: noch kein Hinweis am Tool-Ergebnis.
  for (let i = 100; i < 149; i++) await step(i)
  expect(statuses[statuses.length - 1]).toBe('Antwort 149 von 150')
  expect((await toolCall()).context).toBeUndefined()

  // Antwort 150: der naechste Schritt traegt den Hinweis, ohne etwas zu verbieten.
  await step(149)
  expect(statuses[statuses.length - 1]).toBe('Antwort 150 von 150')
  const late = await toolCall()
  expect(late.deny).toBeUndefined()
  expect(late.context).toEqual([ABSCHLUSS_TEXT])
  expect(toasts.length).toBe(1)
})

test('Engine: Schritte eines Subagenten zaehlen nicht mit', async ($, on) => {
  const statuses: (string | undefined)[] = []
  on('ui.status', (_$, e) => {
    statuses.push(e.text)
    return null as never
  })
  on('turn.step', async function* (_$, e) {
    return { turnId: e.turnId, index: e.index, answer: '', toolUses: [], stopReason: null, usage: null }
  })

  const run = async (extra: object) => {
    const stream = $.turn.step({ ...stepInput(0), ...extra })
    for await (const _chunk of stream) {
      // leer
    }
    await stream.result
  }
  await run({ agentId: 'sub-1' })
  expect(statuses.length).toBe(0)
  await run({})
  expect(statuses).toEqual(['Antwort 1 von 150'])
})
