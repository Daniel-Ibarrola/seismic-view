# Notes

The tests need the depenency "vitest-canvas-mock" to run, because 
chartjs breaks them. However, there is an issue with vitest-canvas-mock because it tries to import
and incorrect module. To fix this issue go to the following file:

```
ew-grapher/node_modules/vitest-canvas-mock/dist/index.js
```

Then look for hte following line:

```javascript
async function importMockWindow() {
  // @ts-expect-error: Missing files
  const getCanvasWindow = await import('jest-canvas-mock/lib/window').then(res => res.default?.default || res.default || res)

  const canvasWindow = getCanvasWindow({ document: window.document })
```
Then add .js extension at the end of jest-canvas-mock/lib/window

```diff
async function importMockWindow() {
  // @ts-expect-error: Missing files
-    const getCanvasWindow = await import('jest-canvas-mock/lib/window').then(res => res.default?.default || res.default || res)
+    const getCanvasWindow = await import('jest-canvas-mock/lib/window.js').then(res => res.default?.default || res.default || res)

  const canvasWindow = getCanvasWindow({ document: window.document })
```
