<?php

// Get some command line ops.
$filename = $argv[1];     // access log to parse
$bucket_size = $argv[2];  // How many millisec per bucket?

if (!$filename || !file_exists($filename) || !$bucket_size) {
    die("Usage: {$argv[0]} filename bucket-size\n");
}

$max_usec = 0;
$buckets = array();

// Read each line into a bucket.
$fh = fopen($filename, "r");
while ($line = fgets($fh)) {
    // Capture 2nd to last integer, convert to ms.
    if (preg_match("/^.* (\d+) \d+\s+$/", $line, $m)) {
        $ms = round($m[1] / 1000);

        // Find appropriate bucket.
        $bucket = (int) (round($ms / $bucket_size) + 1) * $bucket_size;
        if (!array_key_exists($bucket, $buckets)) {
            $buckets[$bucket] = 0;
        }
        $buckets[$bucket]++;
    }
}
fclose($fh);
ksort($buckets);

// Write out all of our counts, filling in any missing buckets..
echo "# ms count \n";
$max_bucket = max(array_keys($buckets));
for ($i = 0; $i <= $max_bucket; $i += $bucket_size) {
    if (!array_key_exists($i, $buckets)) {
        echo "$i 0\n"; // empty buckets
    } else {
        echo "$i {$buckets[$i]}\n";
    }
}

