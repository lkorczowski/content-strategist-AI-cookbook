<?php
/**
 * Plugin Name: Agent Search Endpoint
 * Description: Lets AI agents search this site instead of crawling it. Serves /.well-known/search (Markdown passages from the site's own search) and adds the agent:* discovery meta tags, the same contract as Cloudflare Search for Agents. For sites that are not behind Cloudflare.
 * Version: 1.0.0
 * Author: Dr. Louis Korczowski (content-strategist-AI-cookbook, skill statur-trades-site)
 * License: MIT
 *
 * Install: copy this file to wp-content/mu-plugins/ (create the folder if needed),
 * or zip it and upload it under Plugins > Add New > Upload. No settings.
 * Test:    curl "https://example.com/.well-known/search?q=your+question"
 * Remove:  delete the file. Nothing is stored in the database.
 */

if (!defined('ABSPATH')) {
    exit;
}

const AGENT_SEARCH_PATH = '/.well-known/search';
const AGENT_SEARCH_MAX_RESULTS = 10;
const AGENT_SEARCH_PASSAGE_CHARS = 700;

/** Discovery tags in the head of every HTML page. */
add_action('wp_head', function () {
    $endpoint = home_url(AGENT_SEARCH_PATH) . '?q={query}';
    $instructions = 'To find information on this site, call the search endpoint instead of crawling pages. '
        . 'Replace {query} with a URL-encoded question. Results are Markdown passages with a link to each source page.';
    printf("<meta name=\"agent:instructions\" content=\"%s\" />\n", esc_attr($instructions));
    printf("<meta name=\"agent:endpoint\" content=\"%s\" />\n", esc_attr($endpoint));
    echo "<meta name=\"agent:method\" content=\"GET\" />\n";
}, 1);

/** Best passage of a post for the query: the text around the first matching term. */
function agent_search_passage(string $text, array $terms): string
{
    $text = trim(preg_replace('/\s+/u', ' ', $text));
    $pos = false;
    foreach ($terms as $term) {
        $p = mb_stripos($text, $term);
        if ($p !== false && ($pos === false || $p < $pos)) {
            $pos = $p;
        }
    }
    $start = $pos === false ? 0 : max(0, $pos - intdiv(AGENT_SEARCH_PASSAGE_CHARS, 3));
    $passage = mb_substr($text, $start, AGENT_SEARCH_PASSAGE_CHARS);
    return ($start > 0 ? '...' : '') . $passage . (mb_strlen($text) > $start + AGENT_SEARCH_PASSAGE_CHARS ? '...' : '');
}

/** The endpoint itself. Runs before WordPress looks for a page, so no 404. */
add_action('parse_request', function () {
    $path = (string) wp_parse_url($_SERVER['REQUEST_URI'] ?? '', PHP_URL_PATH);
    $base = rtrim((string) wp_parse_url(home_url('/'), PHP_URL_PATH), '/');
    if (rtrim($path, '/') !== $base . AGENT_SEARCH_PATH) {
        return;
    }

    $method = strtoupper($_SERVER['REQUEST_METHOD'] ?? 'GET');
    $q = '';
    if ($method === 'GET' || $method === 'HEAD') {
        $q = isset($_GET['q']) ? (string) wp_unslash($_GET['q']) : '';
    } elseif ($method === 'QUERY' || $method === 'POST') {
        // HTTP QUERY: plain-text body, or JSON {"q": "..."}.
        $body = (string) file_get_contents('php://input', false, null, 0, 4000);
        $json = json_decode($body, true);
        $q = is_array($json) && isset($json['q']) && is_string($json['q']) ? $json['q'] : $body;
    } else {
        status_header(405);
        header('Allow: GET, HEAD, QUERY, POST');
        exit;
    }
    $q = trim(sanitize_text_field(mb_substr($q, 0, 200)));

    nocache_headers();
    header('Content-Type: text/markdown; charset=utf-8');
    header('X-Robots-Tag: noindex');
    header('Access-Control-Allow-Origin: *');

    $site = wp_strip_all_tags(get_bloginfo('name'));
    if ($q === '') {
        status_header(400);
        echo "# Search {$site}\n\nAdd a query: " . home_url(AGENT_SEARCH_PATH) . "?q=your+question\n";
        exit;
    }

    $query = new WP_Query([
        's' => $q,
        'post_type' => ['post', 'page'],
        'post_status' => 'publish',
        'has_password' => false,
        'posts_per_page' => AGENT_SEARCH_MAX_RESULTS,
        'ignore_sticky_posts' => true,
        'no_found_rows' => true,
    ]);

    status_header(200);
    if ($method === 'HEAD') {
        exit;
    }
    $terms = array_values(array_filter(preg_split('/\s+/u', $q), fn($t) => mb_strlen($t) > 2));
    echo "# Search results for \"" . str_replace('"', "'", $q) . "\" on {$site}\n\n";
    if (!$query->have_posts()) {
        echo "No result. Try other words, or read " . home_url('/') . "\n";
        exit;
    }
    foreach ($query->posts as $i => $post) {
        $title = wp_strip_all_tags(get_the_title($post));
        $text = wp_strip_all_tags(strip_shortcodes((string) $post->post_content));
        $date = get_the_modified_date('Y-m-d', $post);
        echo '## ' . ($i + 1) . '. ' . $title . "\n\n";
        echo 'Source: ' . get_permalink($post) . " (updated {$date})\n\n";
        echo agent_search_passage($text, $terms) . "\n\n";
    }
    exit;
});
