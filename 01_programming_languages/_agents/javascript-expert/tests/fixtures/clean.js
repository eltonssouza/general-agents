// Fixture with no expected findings for scan_js_smells.py
export function sum(a, b) {
  const result = a + b;
  if (Number.isNaN(result)) {
    throw new RangeError("invalid input");
  }
  return result;
}

export const doubled = (list) => list.map((x) => x * 2);
