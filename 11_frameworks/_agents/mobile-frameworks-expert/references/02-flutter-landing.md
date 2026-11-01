# 02 - Flutter: documentation landing page (FLT p.1-4)

**What the source is:** the home page "Flutter documentation" (site capture), **with no version and no printed date** (the PDF metadata indicates capture on Aug 18, 2026, but that is not on the page). It is almost only **navigation**: cards, links and videos. It is not a tutorial. Everything below is paraphrase.

## What the text says
- **Subtitle (FLT p.1):** get started with Flutter; widgets, examples, updates and API docs to write your first app [from source].
- **Navigation cards (FLT p.1):** Install Flutter (set up the environment and get started), Widget catalog (rich set of SDK widgets), API docs (framework reference), Learning resources (tutorials, code samples, workshops and "recipes"), Videos (YouTube channel) and Create with AI (build with and integrate AI tools); "What's new" link for site changes since the last release [from source]. The destinations of these links are **not** in the collection.
- **"New to Flutter?" (FLT p.1):** asks whether the person wants to build beautiful multiplatform apps from **a single codebase**; recommends first setting up the Flutter environment and then following the "Flutter learning pathway" [from source].
- **Coming from another platform (FLT p.1):** there are "Flutter for" pages for **Android, SwiftUI, UIKit, React Native and Xamarin.Forms** developers [from source]. The content of those pages is not in the collection; the list only proves the docs offer them.
- **Building layouts (FLT p.1):** learn to build layouts in Flutter "where everything is a widget" [from source].
- **Understanding constraints (FLT p.1-2):** the summary sentence of the layout model is "Constraints flow down. Sizes flow up. Parents set positions" (FLT p.2, short literal quote); by understanding this, the reader would be on the way to grasping Flutter's layout model [from source]. The text **does not explain** the mechanism beyond that sentence.
- **Adding interactivity (FLT p.2):** learn to add a **stateful widget** to the app [from source]. Nothing beyond the title.
- **FAQ (FLT p.2):** answers to frequently asked questions (content not present) [from source].
- **Videos (FLT p.2-3):** Google I/O technical sessions on Dart and Flutter; a 4-video "Full-stack developer guide" series released at Google I/O, with a closing video on the I/O blog; new videos "almost every week"; link to the YouTube channel [from source]. Session titles appear only in thumbnails (rendered).
- **License (FLT p.4):** unless otherwise noted, the site is under **Creative Commons Attribution 4.0** and the code samples under **3-clause BSD**; Terms, Brand, Privacy, Security links [from source].

## [inference] and limits
- The text mentions **Dart** only when talking about the videos ("Dart and Flutter", FLT p.2). It **does not say** that Dart is Flutter's language: saying so is [extrapolation] (external knowledge).
- "Multiplatform from one codebase" is the text's promise (FLT p.1); which platforms, performance and how it works: NOT COVERED.

## NOT COVERED
Installation, SDK/versions, the Dart language, widget list, `StatelessWidget`/`StatefulWidget` (only the expression "stateful widget"), hot reload, state management, Material/Cupertino, navigation, testing, build/deploy, desktop/web, performance, detailed comparison with React Native/SwiftUI (links only). See also `10-comparacao-rn-flutter-swift.md`.
