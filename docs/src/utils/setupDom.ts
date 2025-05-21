// setupDom.ts
import { JSDOM } from 'jsdom'

export function setupDomEnvironment() {
  const dom = new JSDOM(`<!DOCTYPE html>`)
  globalThis.window = dom.window as any
  globalThis.document = dom.window.document
  globalThis.Node = dom.window.Node
  globalThis.HTMLElement = dom.window.HTMLElement
}