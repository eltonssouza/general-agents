# 06 - Vue 3 introduction guide (VUE3G, 8 pages) [DATED]

Source: the "Introduction" page of the official Vue 3 documentation, captured from the site (PDF from August 2026 according to the metadata; the text does not print the date). Minor version not given. Short content: **it is an overview, not a complete guide**.

## What it is (p.1-2)
- [from source] (VUE3G p.1) Vue (pronounced "view") is a JavaScript framework for interfaces, built on standard HTML, CSS and JavaScript, with a declarative, component-based model.
- [from source] (VUE3G p.1) Notice on the page: "You are reading the documentation for Vue 3"; support for **Vue 2 ended on December 31, 2023**; there is a Migration Guide (link; the content is **not** in the collection).
- [from source] (VUE3G p.1-2) Minimal example: `createApp({ setup() { return { count: ref(0) } } }).mount('#app')` with `<button @click="count++">Count is: {{ count }}</button>`.
- [from source] (VUE3G p.2) Two core features: **declarative rendering** (a template that extends HTML describes the output from the state) and **reactivity** (Vue tracks changes and updates the DOM).
- [from source] (VUE3G p.2) Prerequisite: familiarity with HTML, CSS and JavaScript.

## The progressive framework (p.3)
- [from source] (VUE3G p.3) Vue is "flexible and incrementally adoptable". Uses listed: enhancing static HTML without a build; Web Components; SPA; fullstack/SSR; Jamstack/SSG; desktop, mobile, WebGL and terminal. The core knowledge is shared across these uses.

## Single-File Components (p.3-4)
- [from source] (VUE3G p.3-4) In projects with a build tool, components are written in `.vue` (SFC), which encapsulate logic (JS), template (HTML) and styles (CSS). Recommended when there is a build setup. Vue "takes care of the build tools setup" (p.4).
- [from source] (VUE3G p.4) SFC example: `<script setup>` + `<template>` + `<style scoped>`.

## API styles (p.4-7)
See `07-options-vs-composition.md` for the full comparison.

## Learning paths (p.8)
Tutorial, Guide, Examples (links). Content not included.

## NOT COVERED in this collection
Reactivity in depth, full lifecycle, `computed`/`watch` in the Composition API, `defineProps`/`defineEmits`, slots, Vue Router/Pinia for Vue 3, scaffolding tools (the text only says Vue takes care of the build setup), TypeScript, testing, performance, SSR in plain Vue (only cited as a way of use).
