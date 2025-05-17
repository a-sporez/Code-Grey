<?php
$logFile = __DIR__ . '/messages.txt';
$rssFile = __DIR__ . '/feed.xml';

// Get and normalize message
$message = $_POST['message'] ?? '';
$message = str_replace(["\r\n", "\r"], "\n", $message); // normalize line endings
$message = trim($message);

// Backup original for caching
$rawMessage = $message;

// Sanitize control characters (except newline)
$cleanMessage = preg_replace('/[[:cntrl:]&&[^\n]]/', '', $message);

// Detect base64-like input (long unbroken lines of valid b64 chars)
$isBase64ish = preg_match('/^[A-Za-z0-9+\/=]{100,}$/', str_replace("\n", "", $cleanMessage));

// Provide user feedback
if ($isBase64ish) {
    $cleanMessage = "[Transmission redacted by The Swamp: suspected encoded payload.]\n\n-- Original message retained in the archive.";
}

// Save to log (always store raw message)
$timestamp = date('r');
$entry = "[{$timestamp}] {$rawMessage}\n";
file_put_contents($logFile, $entry, FILE_APPEND);

// Load or create RSS structure
$rss = new DOMDocument();
$rss->load($rssFile);
$channel = $rss->getElementsByTagName('channel')->item(0);

// Create new RSS item
$item = $rss->createElement('item');
$title = $rss->createElement('title', 'New Transmission');

// Escape + preserve line breaks
$desc = $rss->createElement('description');
$descText = $rss->createCDATASection(str_replace("\n", "<br>", htmlspecialchars($cleanMessage)));
$desc->appendChild($descText);

$date = $rss->createElement('pubDate', $timestamp);
$guid = $rss->createElement('guid', 'https://abyss.pond.red/feed/feed.xml#' . time());

$item->appendChild($title);
$item->appendChild($desc);
$item->appendChild($date);
$item->appendChild($guid);

// Insert before first item, or append if none
$firstItem = null;
foreach ($channel->childNodes as $child) {
    if ($child->nodeName === 'item') {
        $firstItem = $child;
        break;
    }
}
if ($firstItem) {
    $channel->insertBefore($item, $firstItem);
} else {
    $channel->appendChild($item);
}

// Save final RSS
$rss->formatOutput = true;
$rss->save($rssFile);

header("Location: form.html");
exit;
?>