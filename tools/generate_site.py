#!/usr/bin/env python3
"""
Generate a static gallery website for EdgeTX Lua scripts.

Reads scripts.json, processes images (copy local, preserve URLs),
and generates a self-contained index.html with Tailwind + Alpine.js.
"""

import json
import sys
import argparse
import shutil
from pathlib import Path


def load_scripts(scripts_json_path: Path) -> list:
    """Load and validate scripts.json."""
    if not scripts_json_path.exists():
        print(f"Error: {scripts_json_path} not found", file=sys.stderr)
        sys.exit(1)

    with open(scripts_json_path, 'r', encoding='utf-8') as f:
        scripts = json.load(f)

    if not isinstance(scripts, list):
        print("Error: scripts.json must be an array", file=sys.stderr)
        sys.exit(1)

    return scripts


def process_images(scripts: list, assets_dir: Path, output_dir: Path) -> None:
    """
    Process images for each script:
    - Copy local files from assets_dir to output_dir/images/
    - Preserve external URLs (http/https)
    - Update script['images'] with new paths
    """
    images_output = output_dir / "images"
    images_output.mkdir(parents=True, exist_ok=True)

    for script in scripts:
        if 'images' not in script:
            script['images'] = []
            continue

        processed_images = []

        for image_path in script['images']:
            # External URL: keep as-is
            if image_path.startswith('http://') or image_path.startswith('https://'):
                processed_images.append(image_path)
                continue

            # Local file: copy and rewrite path
            # image_path is repo-relative (e.g. "ASSETS/foo/shot.jpg"),
            # so resolve from assets_dir's parent (the repo root), not assets_dir itself.
            repo_root = assets_dir.parent.resolve()
            source_path = (repo_root / image_path).resolve()

            # Reject paths outside the repository root
            try:
                source_path.relative_to(repo_root)
            except ValueError:
                print(
                    f"Warning: Skipping out-of-repo image path for '{script.get('name', 'unknown')}': {image_path}",
                    file=sys.stderr
                )
                continue

            if not source_path.exists():
                print(
                    f"Warning: Image not found for '{script.get('name', 'unknown')}': {image_path}",
                    file=sys.stderr
                )
                continue

            # Compute destination: preserve full relative subdirectory structure
            # e.g., ASSETS/foo/bar/screenshot-1.jpg -> images/ASSETS/foo/bar/screenshot-1.jpg
            relative_path = Path(image_path)
            dest_path = images_output / relative_path
            dest_path.parent.mkdir(parents=True, exist_ok=True)

            try:
                shutil.copy2(source_path, dest_path)
                # Store relative path from the perspective of output_dir root
                new_image_path = str(dest_path.relative_to(output_dir)).replace('\\', '/')
                processed_images.append(new_image_path)
            except Exception as e:
                print(
                    f"Warning: Failed to copy image '{image_path}' for '{script.get('name', 'unknown')}': {e}",
                    file=sys.stderr
                )

        script['images'] = processed_images


def get_categories(scripts: list) -> list:
    """Extract and sort unique categories."""
    categories = set()
    for script in scripts:
        if 'category' in script:
            categories.add(script['category'])
    return sorted(categories)


def get_all_tags(scripts: list) -> list:
    """Extract and sort unique tags across all scripts."""
    tags = set()
    for script in scripts:
        if 'tags' in script and isinstance(script['tags'], list):
            tags.update(script['tags'])
    return sorted(tags)


def generate_html(scripts: list, categories: list, all_tags: list) -> str:
    """Generate the complete HTML file."""

    # Convert data to JSON strings
    def _safe_json(obj) -> str:
        return json.dumps(obj, ensure_ascii=False).replace('</script>', '<\\/script>')

    scripts_json = _safe_json(scripts)
    categories_json = _safe_json(categories)
    all_tags_json = _safe_json(all_tags)

    # HTML template with placeholders (avoiding f-string brace conflicts)
    html_template = """<!DOCTYPE html>
<html lang="en" x-data="gallery()" :class="darkMode ? 'dark' : ''" x-cloak>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EdgeTX Lua Scripts Gallery</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>tailwind.config = { darkMode: 'class' }</script>
    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.14.9/dist/cdn.min.js"></script>
    <style>
        [x-cloak] { display: none !important; }
        .edgetx-color { --edgetx: #e03c3c; }
        :root { --edgetx: #e03c3c; }
    </style>
</head>
<body class="bg-gray-100 dark:bg-gray-900 text-gray-900 dark:text-gray-100 min-h-screen edgetx-color">

    <!-- Header -->
    <header class="bg-white dark:bg-gray-800 shadow-sm sticky top-0 z-40">
        <div class="max-w-7xl mx-auto px-4 py-3 sm:px-6 lg:px-8 flex items-center justify-between gap-4">
            <div class="flex items-center gap-3">
                <h1 class="text-2xl font-bold">EdgeTX Lua Scripts</h1>
                <span class="text-sm text-gray-500 dark:text-gray-400" x-text="`(${scripts.length})`"></span>
            </div>

            <div class="flex-1 max-w-xs">
                <input
                    type="text"
                    x-model="search"
                    placeholder="Search scripts..."
                    class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
                >
            </div>

            <button
                @click="darkMode = !darkMode; localStorage.setItem('darkMode', darkMode)"
                class="p-2 hover:bg-gray-200 dark:hover:bg-gray-700 rounded-lg transition"
                :aria-label="darkMode ? 'Light mode' : 'Dark mode'"
            >
                <template x-if="darkMode">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M12 3v2.25m6.364.386-1.591 1.591M21 12h-2.25m-.386 6.364-1.591-1.591M12 18.75V21m-4.773-4.227-1.591 1.591M5.25 12H3m4.227-4.773L5.636 5.636M15.75 12a3.75 3.75 0 1 1-7.5 0 3.75 3.75 0 0 1 7.5 0Z"/>
                    </svg>
                </template>
                <template x-if="!darkMode">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M21.752 15.002A9.72 9.72 0 0 1 18 15.75c-5.385 0-9.75-4.365-9.75-9.75 0-1.33.266-2.597.748-3.752A9.753 9.753 0 0 0 3 11.25C3 16.635 7.365 21 12.75 21a9.753 9.753 0 0 0 9.002-5.998Z"/>
                    </svg>
                </template>
            </button>
        </div>
    </header>

    <!-- Filters Bar -->
    <div class="sticky top-[57px] z-30 bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 shadow-sm">
        <div class="max-w-7xl mx-auto px-4 py-4 sm:px-6 lg:px-8">
            <!-- Category Tabs (horizontally scrollable) -->
            <div class="mb-4">
                <div class="flex gap-2 overflow-x-auto pb-2">
                    <button
                        @click="activeCategory = null"
                        :class="activeCategory === null ? 'bg-red-600 text-white' : 'bg-gray-200 dark:bg-gray-700 text-gray-900 dark:text-gray-100 hover:bg-gray-300 dark:hover:bg-gray-600'"
                        class="px-4 py-2 rounded-full whitespace-nowrap font-medium transition text-sm"
                    >
                        All
                    </button>
                    <template x-for="cat in categories" :key="cat">
                        <button
                            @click="activeCategory = activeCategory === cat ? null : cat"
                            :class="activeCategory === cat ? 'bg-red-600 text-white' : 'bg-gray-200 dark:bg-gray-700 text-gray-900 dark:text-gray-100 hover:bg-gray-300 dark:hover:bg-gray-600'"
                            class="px-4 py-2 rounded-full whitespace-nowrap font-medium transition text-sm"
                            x-text="cat"
                        ></button>
                    </template>
                </div>
            </div>

            <!-- Tag Chips (wrapping) -->
            <div class="flex flex-wrap gap-2">
                <template x-for="tag in allTags" :key="tag">
                    <button
                        @click="toggleTag(tag)"
                        :class="activeTags.includes(tag) ? 'bg-red-100 dark:bg-red-900/40 text-red-700 dark:text-red-300 border-red-600' : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 border-gray-300 dark:border-gray-600 hover:border-red-600'"
                        class="px-3 py-1 rounded-full text-xs font-medium border transition cursor-pointer"
                        x-text="tag"
                    ></button>
                </template>
            </div>
        </div>
    </div>

    <!-- Results Count -->
    <div class="max-w-7xl mx-auto px-4 py-3 sm:px-6 lg:px-8 text-sm text-gray-600 dark:text-gray-400">
        <span x-text="`${filtered.length} script${filtered.length !== 1 ? 's' : ''} found`"></span>
    </div>

    <!-- Gallery Grid -->
    <main class="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <template x-for="(script, si) in filtered" :key="script.name">
                <div x-data="card(script, si)" class="bg-white dark:bg-gray-800 rounded-xl shadow-sm hover:shadow-md transition flex flex-col overflow-hidden">

                    <!-- Image Carousel -->
                    <div
                        class="relative bg-gray-900 aspect-video overflow-hidden"
                        @mouseenter="pauseAuto()"
                        @mouseleave="resumeAuto()"
                    >
                        <template x-if="script.images.length === 0">
                            <div class="w-full h-full flex flex-col items-center justify-center gap-2">
                                <svg class="w-12 h-12 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                                </svg>
                                <span class="text-gray-500 text-sm">No screenshot</span>
                            </div>
                        </template>

                        <template x-if="script.images.length > 0">
                            <div>
                                <!-- Current Image -->
                                <img
                                    :src="script.images[currentIndex]"
                                    :alt="`${script.name} screenshot ${currentIndex + 1}`"
                                    class="w-full h-full object-cover cursor-pointer"
                                    @click="window.dispatchEvent(new CustomEvent('open-lightbox', { detail: { script, index: currentIndex } }))"
                                >

                                <!-- Prev/Next Arrows (only if multiple images) -->
                                <template x-if="script.images.length > 1">
                                    <div class="contents">
                                        <button
                                            @click="prev()"
                                            class="absolute left-2 top-1/2 -translate-y-1/2 bg-black/50 hover:bg-black/70 text-white p-2 rounded-full transition"
                                            aria-label="Previous image"
                                        >
                                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
                                            </svg>
                                        </button>
                                        <button
                                            @click="next()"
                                            class="absolute right-2 top-1/2 -translate-y-1/2 bg-black/50 hover:bg-black/70 text-white p-2 rounded-full transition"
                                            aria-label="Next image"
                                        >
                                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
                                            </svg>
                                        </button>

                                        <!-- Dot Indicators -->
                                        <div class="absolute bottom-2 left-1/2 -translate-x-1/2 flex gap-1">
                                            <template x-for="(_, i) in script.images" :key="i">
                                                <button
                                                    @click="goTo(i)"
                                                    :class="currentIndex === i ? 'bg-white' : 'bg-white/50'"
                                                    class="w-2 h-2 rounded-full transition"
                                                    :aria-label="`Go to image ${i + 1}`"
                                                ></button>
                                            </template>
                                        </div>
                                    </div>
                                </template>
                            </div>
                        </template>
                    </div>

                    <!-- Card Body -->
                    <div class="p-4 flex flex-col gap-2 flex-1">
                        <h3 class="font-bold text-lg">
                            <template x-if="script.infourl">
                                <a :href="script.infourl" target="_blank" rel="noopener noreferrer" class="text-red-600 dark:text-red-400 hover:underline flex items-center gap-1">
                                    <span x-text="script.name"></span>
                                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4m-4-6l6 6m0 0l-6 6m6-6H9"/>
                                    </svg>
                                </a>
                            </template>
                            <template x-if="!script.infourl">
                                <span x-text="script.name"></span>
                            </template>
                        </h3>

                        <span class="inline-flex w-fit px-2 py-0.5 rounded-full text-xs font-medium bg-red-100 dark:bg-red-900/40 text-red-700 dark:text-red-300">
                            <span x-text="script.category"></span>
                        </span>

                        <p class="text-sm text-gray-600 dark:text-gray-300 flex-1">
                            <span x-text="script.description"></span>
                        </p>

                        <div class="flex flex-wrap gap-1">
                            <template x-for="tag in script.tags" :key="tag">
                                <button
                                    @click="window.dispatchEvent(new CustomEvent('filter-tag', { detail: { tag } }))"
                                    class="px-2 py-1 text-xs rounded border border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-700 hover:bg-gray-100 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-300 transition cursor-pointer"
                                    x-text="tag"
                                ></button>
                            </template>
                        </div>
                    </div>
                </div>
            </template>
        </div>

        <!-- Empty State -->
        <template x-if="filtered.length === 0">
            <div class="text-center py-12">
                <svg class="w-16 h-16 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
                <p class="text-lg text-gray-600 dark:text-gray-400">No scripts match your filters.</p>
            </div>
        </template>
    </main>

    <!-- Lightbox Modal -->
    <div
        x-data="lightbox()"
        @window:open-lightbox="openWith($event.detail)"
        @window:filter-tag="toggleTag($event.detail.tag)"
        x-show="open"
        class="fixed inset-0 bg-black/90 z-50 flex items-center justify-center p-4"
        @keydown.window.escape="close()"
        @keydown.window.left="prev()"
        @keydown.window.right="next()"
    >
        <template x-if="open">
            <div class="relative w-full h-full flex flex-col items-center justify-center max-w-4xl">
                <!-- Image -->
                <img
                    :src="images[index]"
                    :alt="`${scriptName} screenshot ${index + 1}`"
                    class="max-w-full max-h-[85vh] object-contain"
                >

                <!-- Image Counter -->
                <div class="absolute top-4 right-4 bg-black/50 text-white px-3 py-1 rounded-full text-sm">
                    <span x-text="`${index + 1} / ${images.length}`"></span>
                </div>

                <!-- Close Button -->
                <button
                    @click="close()"
                    class="absolute top-4 left-4 bg-black/50 hover:bg-black/70 text-white p-2 rounded-full transition"
                    aria-label="Close lightbox"
                >
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                    </svg>
                </button>

                <!-- Prev/Next Buttons -->
                <template x-if="images.length > 1">
                    <div class="contents">
                        <button
                            @click="prev()"
                            class="absolute left-4 top-1/2 -translate-y-1/2 bg-black/50 hover:bg-black/70 text-white p-3 rounded-full transition"
                            aria-label="Previous image"
                        >
                            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
                            </svg>
                        </button>
                        <button
                            @click="next()"
                            class="absolute right-4 top-1/2 -translate-y-1/2 bg-black/50 hover:bg-black/70 text-white p-3 rounded-full transition"
                            aria-label="Next image"
                        >
                            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
                            </svg>
                        </button>
                    </div>

                    <!-- Dot Indicators -->
                    <div class="absolute bottom-4 left-1/2 -translate-x-1/2 flex gap-2">
                        <template x-for="(_, i) in images" :key="i">
                            <button
                                @click="index = i"
                                :class="index === i ? 'bg-white' : 'bg-white/50'"
                                class="w-3 h-3 rounded-full transition"
                                :aria-label="`Go to image ${i + 1}`"
                            ></button>
                        </template>
                    </div>
                </template>
            </div>
        </template>
    </div>

    <!-- JavaScript -->
    <script>
        const SCRIPTS = ___SCRIPTS_JSON___;
        const CATEGORIES = ___CATEGORIES_JSON___;
        const ALL_TAGS = ___ALL_TAGS_JSON___;

        function gallery() {
            return {
                scripts: SCRIPTS,
                categories: CATEGORIES,
                allTags: ALL_TAGS,
                search: '',
                activeCategory: null,
                activeTags: [],
                darkMode: localStorage.getItem('darkMode') === 'true',

                get filtered() {
                    return this.scripts.filter(script => {
                        // Filter by category
                        if (this.activeCategory !== null && script.category !== this.activeCategory) {
                            return false;
                        }

                        // Filter by tags (AND — must have all active tags)
                        if (this.activeTags.length > 0) {
                            const scriptTags = script.tags || [];
                            const hasAllTags = this.activeTags.every(tag => scriptTags.includes(tag));
                            if (!hasAllTags) {
                                return false;
                            }
                        }

                        // Filter by search (case-insensitive, name or description)
                        if (this.search.trim() !== '') {
                            const searchLower = this.search.toLowerCase();
                            const matchesName = (script.name || '').toLowerCase().includes(searchLower);
                            const matchesDesc = (script.description || '').toLowerCase().includes(searchLower);
                            if (!matchesName && !matchesDesc) {
                                return false;
                            }
                        }

                        return true;
                    });
                },

                toggleTag(tag) {
                    const index = this.activeTags.indexOf(tag);
                    if (index > -1) {
                        this.activeTags.splice(index, 1);
                    } else {
                        this.activeTags.push(tag);
                    }
                },

                init() {
                    // Listen for filter-tag events from tag chips
                    window.addEventListener('filter-tag', (e) => {
                        this.toggleTag(e.detail.tag);
                    });
                }
            };
        }

        function card(script, si) {
            return {
                script,
                currentIndex: 0,
                timer: null,

                init() {
                    if (script.images.length > 1) {
                        this.startAuto();
                    }
                },

                destroy() {
                    this.pauseAuto();
                },

                startAuto() {
                    this.pauseAuto();
                    this.timer = setInterval(() => {
                        this.next();
                    }, 4000 + si * 200);
                },

                pauseAuto() {
                    if (this.timer) {
                        clearInterval(this.timer);
                        this.timer = null;
                    }
                },

                resumeAuto() {
                    if (this.script.images.length > 1 && this.timer === null) {
                        this.startAuto();
                    }
                },

                prev() {
                    this.currentIndex = (this.currentIndex - 1 + this.script.images.length) % this.script.images.length;
                },

                next() {
                    this.currentIndex = (this.currentIndex + 1) % this.script.images.length;
                },

                goTo(i) {
                    this.currentIndex = i;
                    this.pauseAuto();
                    this.resumeAuto();
                }
            };
        }

        function lightbox() {
            return {
                open: false,
                images: [],
                index: 0,
                scriptName: '',

                openWith(data) {
                    this.images = data.script.images;
                    this.scriptName = data.script.name;
                    this.index = data.index;
                    this.open = true;
                },

                close() {
                    this.open = false;
                },

                prev() {
                    this.index = (this.index - 1 + this.images.length) % this.images.length;
                },

                next() {
                    this.index = (this.index + 1) % this.images.length;
                }
            };
        }
    </script>
</body>
</html>"""

    # Replace placeholders with actual JSON
    html_output = html_template.replace('___SCRIPTS_JSON___', scripts_json)
    html_output = html_output.replace('___CATEGORIES_JSON___', categories_json)
    html_output = html_output.replace('___ALL_TAGS_JSON___', all_tags_json)

    return html_output


def main():
    parser = argparse.ArgumentParser(
        description='Generate a static gallery website for EdgeTX Lua scripts.'
    )
    parser.add_argument(
        '--scripts-json',
        type=Path,
        default=Path('scripts.json'),
        help='Path to scripts.json (default: scripts.json)'
    )
    parser.add_argument(
        '--assets-dir',
        type=Path,
        default=Path('ASSETS'),
        help='Path to assets directory (default: ASSETS)'
    )
    parser.add_argument(
        '--output-dir',
        type=Path,
        default=Path('site'),
        help='Output directory for generated site (default: site)'
    )

    args = parser.parse_args()

    # Resolve paths relative to CWD
    scripts_json_path = args.scripts_json.resolve()
    assets_dir = args.assets_dir.resolve()
    output_dir = args.output_dir.resolve()

    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load scripts
    scripts = load_scripts(scripts_json_path)

    # Process images
    process_images(scripts, assets_dir, output_dir)

    # Extract categories and tags
    categories = get_categories(scripts)
    all_tags = get_all_tags(scripts)

    # Generate HTML
    html_content = generate_html(scripts, categories, all_tags)

    # Write index.html
    index_path = output_dir / 'index.html'
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"Site generated in {output_dir}/")


if __name__ == '__main__':
    main()
