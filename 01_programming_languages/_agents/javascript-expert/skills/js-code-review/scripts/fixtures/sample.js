// Test fixture for scan_js_smells.py
var total = 0;

function process(items, input) {
  if (input == "") {
    return [];
  }
  if (isNaN(input)) {
    return null;
  }
  items.forEach(async (item) => {
    total += await fetchValue(item);
  });
  for (const key in items) {
    console.log(key);
  }
  try {
    const data = eval("(" + input + ")");
    return data.values.sort();
  } catch (e) {}
}
