const CACHE_NAME = "ai-trading-assistant-v1.0.1";

const FILES_TO_CACHE = [
    "./",
    "./index.html",
    "./watchlist.html",
    "./settings.html",
    "./offline.html",
    "./manifest.json",
    "./css/style.css",
    "./js/common.js",
    "./js/app.js",
    "./icons/icon-192.png",
    "./icons/icon-512.png"
];

// ======================================
// Install
// ======================================

self.addEventListener("install", event => {

    event.waitUntil(

        caches.open(CACHE_NAME)

        .then(cache => cache.addAll(FILES_TO_CACHE))

    );

    self.skipWaiting();

});

// ======================================
// Activate
// ======================================

self.addEventListener("activate", event => {

    event.waitUntil(

        caches.keys()

        .then(keys =>

            Promise.all(

                keys.map(key => {

                    if (key !== CACHE_NAME) {

                        return caches.delete(key);

                    }

                })

            )

        )

    );

    self.clients.claim();

});

// ======================================
// Fetch
// ======================================

self.addEventListener("fetch", event => {

    if (event.request.method !== "GET") {

        return;

    }

    event.respondWith(

        caches.match(event.request)

        .then(cachedResponse => {

            if (cachedResponse) {

                return cachedResponse;

            }

            return fetch(event.request)

            .then(networkResponse => {

                if (

                    !networkResponse ||

                    networkResponse.status !== 200

                ) {

                    return networkResponse;

                }

                const responseClone = networkResponse.clone();

                caches.open(CACHE_NAME)

                .then(cache => {

                    cache.put(

                        event.request,

                        responseClone

                    );

                });

                return networkResponse;

            })

            .catch(() => {

                if (

                    event.request.destination === "document"

                ) {

                    return caches.match("./offline.html");

                }

            });

        })

    );

});

// ======================================
// Push Notifications
// ======================================

self.addEventListener("push", event => {

    let data = {

        title: "AI Trading Assistant",

        body: "A new trading signal is available.",

        icon: "./icons/icon-192.png",

        badge: "./icons/icon-72.png"

    };

    if (event.data) {

        try {

            data = event.data.json();

        }

        catch {

            data.body = event.data.text();

        }

    }

    event.waitUntil(

        self.registration.showNotification(

            data.title,

            {

                body: data.body,

                icon: data.icon,

                badge: data.badge,

                vibrate: [200, 100, 200],

                requireInteraction: true

            }

        )

    );

});

// ======================================
// Notification Click
// ======================================

self.addEventListener("notificationclick", event => {

    event.notification.close();

    event.waitUntil(

        clients.matchAll({

            type: "window",

            includeUncontrolled: true

        })

        .then(clientList => {

            for (const client of clientList) {

                if ("focus" in client) {

                    return client.focus();

                }

            }

            if (clients.openWindow) {

                return clients.openWindow("./index.html");

            }

        })

    );

});