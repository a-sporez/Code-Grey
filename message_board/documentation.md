# Documentation for the website

## **Reference sheet** describes

* Each file’s purpose
* What variables exist and why
* What the logic blocks are doing
* How the system behaves from request to render

---

### 🌀 Abyss Transmission Engine – Internal Reference Manual

#### 🌐 `feed.html` – Transmission Viewer

**Purpose:** Displays messages from `feed.xml` using JavaScript and DOM manipulation.

**Key Flow:**

* Loads `feed.xml` via `fetch()`
* Parses it as XML
* Iterates over `<item>` elements
* Extracts:

  * `<title>` → shown bold
  * `<description>` → processed to preserve line breaks
  * `<pubDate>` → shown as a timestamp

**DOM Structure Per Entry:**

```html
<div class="entry">
  <div><strong>Title</strong></div>
  <div class="description">Message body (with line breaks)</div>
  <div class="timestamp">Date</div>
</div>
```

**Important JS Behaviors:**

* `description.replace(/\n/g, "<br>")`: converts newlines into visible HTML
* Everything appended to `#feed` container
* Uses CSS classes to control layout

---

#### 📜 `style.css` – Visual Theme

**Purpose:** Controls layout and readability for the entire site.

**Key Variables:**

* `--text-color`, `--background-color`, etc. → theme colors
* `--font-main`, `--font-secondary` → fonts for headings/body

**Important Classes:**

* `.entry` – the message wrapper
* `.description` – the message body

  * Uses `white-space: pre-wrap` to show line breaks
  * `max-height + overflow: auto` for long messages
* `.timestamp` – faded timestamp
* `.glitch` (optional) – visual styling for corrupted transmissions

---

#### 🧾 `messages.txt` – Message Archive

**Purpose:** Stores **every raw message** exactly as submitted, with a timestamp.

**Format:**

```txt
[Fri, 17 May 2025 02:31:08 +0000] The Pond speaks again...
```

**Used For:**

* Developer logs
* ARG lore continuity
* Forensics if the XML breaks

---

#### 📮 `form.html` – Message Submission UI

**Purpose:** Allows users to submit anonymous text to the system via POST to `submit.php`.

**Elements:**

* `<textarea name="message">` – the actual input
* `<form method="POST" action="submit.php">` – sends to PHP backend
* Styled with `style.css`

---

#### 🧠 `submit.php` – Core Message Handler

**Purpose:** Receives the message, stores it, sanitizes it, and updates the RSS feed.

---

### 🌊 `submit.php` Behavior Breakdown

* **Load the submitted message**

```php
$message = $_POST['message'] ?? '';
```

* **Normalize line endings**

```php
$message = str_replace(["\r\n", "\r"], "\n", $message);
```

* **Strip leading/trailing space**

```php
$message = trim($message);
```

* **Preserve original for `messages.txt`**

```php
$rawMessage = $message;
```

* **Sanitize control characters (except \n)**

```php
$cleanMessage = preg_replace('/[[:cntrl:]&&[^\n]]/', '', $message);
```

* **Detect base64-like abuse**

```php
$isBase64ish = preg_match('/^[A-Za-z0-9+\/=]{100,}$/', str_replace("\n", "", $cleanMessage));
if ($isBase64ish) {
  $cleanMessage = "[Transmission redacted by The Swamp: suspected encoded payload.]\n\n-- Original message retained in the archive.";
}
```

* **Log raw message**

```php
$entry = "[{$timestamp}] {$rawMessage}\n";
file_put_contents($logFile, $entry, FILE_APPEND);
```

* **Build a new `<item>` for RSS**

```php
$desc = $rss->createElement('description');
$descText = $rss->createCDATASection(str_replace("\n", "<br>", htmlspecialchars($cleanMessage)));
$desc->appendChild($descText);
```

* **Insert the item at the top**

```php
$channel->insertBefore($item, $firstItem ?? null);
```

* **Save updated RSS**

```php
$rss->save($rssFile);
```

---

### 🧷 Variables Glossary

| Variable        | Purpose                          |
| --------------- | -------------------------------- |
| `$message`      | Normalized user input            |
| `$rawMessage`   | Original input, saved to log     |
| `$cleanMessage` | Sanitized message for RSS        |
| `$timestamp`    | Used in log + `<pubDate>`        |
| `$isBase64ish`  | Flag if message looks encoded    |
| `$descText`     | Final CDATA XML-safe description |

---

### 🧼 Protection Summary

* 🔒 Normalizes weird Windows `^M`
* 🔒 Strips control chars like `\x00`, `\x1F`
* 🔒 Detects & redacts base64-looking blobs
* ✅ Logs everything in full to `messages.txt`
* ✅ Keeps visual display safe using CDATA + `<br>`

---

Would you like a printable or Bear Blog–style version of this sheet too? I can help you port it into your site's `/docs` section if you want to turn this into in-universe dev lore (“Swamp Control Protocols”) 🌿
