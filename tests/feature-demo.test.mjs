import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import vm from "node:vm";
import test from "node:test";

const html = await readFile(new URL("../web/feature-demo.html", import.meta.url), "utf8");
const sample = await readFile(new URL("../web/examples/shape-hunt.v1.json", import.meta.url), "utf8");
const script = /<script>\s*([\s\S]*?)<\/script>/i.exec(html)?.[1];
assert.ok(script, "embedded demo script is available");

const elementIds = [
  "load", "status", "activity", "progress", "step-title",
  "step-hint", "found", "skip", "summary", "result", "again"
];

function createHarness(body = sample, responseInit = {}, chunks = null) {
  const elements = Object.fromEntries(elementIds.map((id) => {
    const listeners = new Map();
    return [id, {
      textContent: "",
      hidden: false,
      disabled: false,
      addEventListener: (name, handler) => listeners.set(name, handler),
      click: () => {
        const handler = listeners.get("click");
        assert.equal(typeof handler, "function", id + " click handler");
        return handler();
      }
    }];
  }));

  const requests = [];
  const streamStats = { cancelled: 0 };
  const fetch = async (url, init) => {
    requests.push({ url, init });
    let nextChunk = 0;
    const responseBody = chunks === null ? body : new ReadableStream({
      pull(controller) {
        if (nextChunk >= chunks.length) {
          controller.close();
          return;
        }
        controller.enqueue(new TextEncoder().encode(chunks[nextChunk++]));
      },
      cancel() {
        streamStats.cancelled += 1;
      }
    });
    return new Response(responseBody, responseInit);
  };
  const document = {
    getElementById: (id) => {
      assert.ok(elements[id], "known element " + id);
      return elements[id];
    }
  };

  vm.runInNewContext(script, { document, fetch, TextDecoder }, { timeout: 2000 });
  return { elements, requests, streamStats };
}

test("valid same-origin JSON renders after the user requests it", async () => {
  const { elements, requests } = createHarness();
  assert.equal(requests.length, 0);
  await elements.load.click();
  assert.equal(requests.length, 1);
  assert.equal(requests[0].url, "./examples/shape-hunt.v1.json");
  assert.equal(requests[0].init.credentials, "omit");
  assert.equal(elements.activity.hidden, false);
  assert.equal(elements["step-title"].textContent, "Spot a circular shape.");
  elements.found.click();
  elements.skip.click();
  elements.found.click();
  assert.equal(elements.summary.hidden, false);
  assert.match(elements.result.textContent, /You found 2 of 3 shapes/);
  elements.again.click();
  assert.equal(elements.activity.hidden, false);
  assert.equal(elements["step-title"].textContent, "Spot a circular shape.");
});

test("unknown renderer, schema, and extra fields all fail closed", async () => {
  const mutate = [
    (pack) => { pack.renderer = "arbitrary-code/v1"; },
    (pack) => { pack.schema = "other"; },
    (pack) => { pack.steps[0].externalUrl = "https://example.org/"; },
    (pack) => { pack.steps[1].id = pack.steps[0].id; }
  ];
  for (const change of mutate) {
    const pack = JSON.parse(sample);
    change(pack);
    const { elements } = createHarness(JSON.stringify(pack));
    await elements.load.click();
    assert.equal(elements.activity.hidden, true);
    assert.match(elements.status.textContent, /unavailable or invalid/);
  }
});

test("markup-like downloaded text remains inert, not injected as HTML", async () => {
  const pack = JSON.parse(sample);
  pack.steps[0].prompt = "<img src=x onerror=alert(1)>";
  const { elements } = createHarness(JSON.stringify(pack));
  await elements.load.click();
  assert.equal(elements["step-title"].textContent, "<img src=x onerror=alert(1)>");
});

test("valid oversized JSON streamed in chunks is rejected by byte limit", async () => {
  // Whitespace padding keeps the fixture syntactically valid. Without the
  // streamed byte bound, JSON.parse would succeed and activate this feature.
  const padding = " ".repeat(13000);
  const oversized = sample + padding;
  assert.doesNotThrow(() => JSON.parse(oversized));
  assert.ok(Buffer.byteLength(oversized) > 12000);

  const chunks = [sample, padding.slice(0, 5900), padding.slice(5900)];
  const { elements, requests } = createHarness(oversized, {}, chunks);
  await elements.load.click();
  assert.equal(requests.length, 1);
  assert.equal(elements.activity.hidden, true);
  assert.match(elements.status.textContent, /unavailable or invalid/);
});

test("oversized Content-Length rejects and cancels its unread response", async () => {
  const { elements, streamStats } = createHarness(
    sample,
    { headers: { "content-length": "13000" } },
    [sample, " ".repeat(130000)]
  );
  await elements.load.click();
  assert.equal(elements.activity.hidden, true);
  assert.equal(streamStats.cancelled, 1);
  assert.match(elements.status.textContent, /unavailable or invalid/);
});

test("HTTP errors cancel unread response bodies before rejecting", async () => {
  const { elements, streamStats } = createHarness(sample, { status: 404 }, [sample, " ".repeat(130000)]);
  await elements.load.click();
  assert.equal(elements.activity.hidden, true);
  assert.equal(streamStats.cancelled, 1);
  assert.match(elements.status.textContent, /unavailable or invalid/);
});

test("missing response body fails closed", async () => {
  const { elements } = createHarness(sample, { status: 204 });
  await elements.load.click();
  assert.equal(elements.activity.hidden, true);
  assert.match(elements.status.textContent, /unavailable or invalid/);
});

test("invalid JSON and a failed HTTP response do not activate a feature", async () => {
  for (const [body, init] of [
    ["{ bad json", {}],
    [sample, { status: 404 }]
  ]) {
    const { elements } = createHarness(body, init);
    await elements.load.click();
    assert.equal(elements.activity.hidden, true);
    assert.match(elements.status.textContent, /unavailable or invalid/);
  }
});
