// Service personnalisé Flowbite pour tarteaucitron
tarteaucitron.services.flowbite = {
    "key": "flowbite",
    "type": "other",
    "name": "Flowbite",
    "uri": "https://flowbite.com/",
    "needConsent": true,
    "cookies": [],
    "js": function () {
        "use strict";
        if (tarteaucitron.user.flowbite) {
            tarteaucitron.user.flowbite();
        }
    }
};

