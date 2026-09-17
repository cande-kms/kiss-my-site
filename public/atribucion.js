/*!
 * atribucion.js — captura de origen de tráfico para formularios
 * ------------------------------------------------------------------
 * Guarda de qué campaña y de qué TÉRMINO DE BÚSQUEDA vino cada visitante,
 * y lo inyecta en los campos ocultos del formulario antes de que se envíe.
 *
 * Funciona igual en WordPress y en un sitio de archivos sueltos.
 * No depende de jQuery ni de ninguna librería.
 *
 * Versión 1.0 — 2026-08-15
 */
(function (window, document) {
  'use strict';

  /* ================== CONFIGURACIÓN ================== */
  var CFG = {
    // Identificador del cliente/sitio. Viaja en cada envío para poder separar
    // varios sitios en un mismo backend. Cambiar en cada implementación.
    SITIO: 'kissmy-site',

    // Días que dura la atribución guardada. 90 es un buen default para
    // servicios B2B con ciclo de venta largo; 30 alcanza para ecommerce.
    DIAS: 90,

    // Regla de atribución:
    //   'primero' = gana la primera visita (recomendado: mide qué canal
    //               DESCUBRE al cliente)
    //   'ultimo'  = gana la última visita (coincide con lo que reporta Google Ads)
    MODELO: 'primero',

    // Clave en localStorage. Cambiarla si conviven dos sistemas.
    CLAVE: 'attr_v1',

    // Escribir también una cookie de primer nivel. Solo hace falta si el
    // backend tiene que leer la atribución del lado del servidor (PHP), o si
    // el sitio usa subdominios (www.cliente.com y app.cliente.com).
    COOKIE: false,
    COOKIE_DOMINIO: '',   // ej: '.cliente.com' para compartir entre subdominios

    // true durante la implementación para ver el log en la consola.
    DEBUG: false
  };

  // Parámetros que se capturan de la URL.
  // Los primeros son IDs de clic de cada plataforma; los utm_* son manuales.
  var PARAMS = [
    'gclid',     // Google Ads
    'gbraid',    // Google Ads — tráfico de apps iOS
    'wbraid',    // Google Ads — web iOS con restricción de cookies
    'fbclid',    // Meta Ads
    'msclkid',   // Microsoft Ads / Bing
    'ttclid',    // TikTok Ads
    'li_fat_id', // LinkedIn Ads
    'utm_source', 'utm_medium', 'utm_campaign',
    'utm_term',  // el término de búsqueda
    'utm_content'
  ];

  // Campos derivados que también se guardan y se pueden inyectar en el form.
  var DERIVADOS = ['landing_inicial', 'referrer_inicial', 'primera_visita'];

  var TODOS = PARAMS.concat(DERIVADOS);

  /* ================== UTILIDADES ================== */

  function log() {
    if (CFG.DEBUG && window.console) {
      console.log.apply(console, ['[atribucion]'].concat([].slice.call(arguments)));
    }
  }

  // Los valores vienen de la URL, o sea que los controla quien arma el link.
  // Se limitan en largo y se limpian de caracteres peligrosos antes de guardar.
  var PELIGROSOS = /[<>"'`\\]/g;
  function limpiar(v) {
    return String(v).slice(0, 300).replace(PELIGROSOS, '');
  }

  function leerStorage() {
    try {
      return JSON.parse(window.localStorage.getItem(CFG.CLAVE) || '{}');
    } catch (e) {
      // Safari en modo privado y algunos navegadores tiran excepción
      return {};
    }
  }

  function escribirStorage(obj) {
    try {
      window.localStorage.setItem(CFG.CLAVE, JSON.stringify(obj));
    } catch (e) {
      log('no se pudo escribir en localStorage:', e.message);
    }
  }

  function escribirCookie(obj) {
    if (!CFG.COOKIE) return;
    try {
      var valor = encodeURIComponent(JSON.stringify(obj));
      var vence = new Date(Date.now() + CFG.DIAS * 864e5).toUTCString();
      var dominio = CFG.COOKIE_DOMINIO ? '; domain=' + CFG.COOKIE_DOMINIO : '';
      document.cookie = CFG.CLAVE + '=' + valor + '; expires=' + vence +
                        '; path=/' + dominio + '; SameSite=Lax';
    } catch (e) {
      log('no se pudo escribir la cookie:', e.message);
    }
  }

  /* ================== CAPTURA ================== */

  function deLaUrl() {
    var out = {};
    var qs = window.location.search;
    if (!qs || qs.length < 2) return out;

    // Parseo manual en vez de URLSearchParams por compatibilidad con IE11
    qs.substring(1).split('&').forEach(function (par) {
      var i = par.indexOf('=');
      if (i < 0) return;
      var k, v;
      try {
        k = decodeURIComponent(par.substring(0, i));
        v = decodeURIComponent(par.substring(i + 1).replace(/\+/g, ' '));
      } catch (e) {
        return;   // porcentajes mal formados en la URL
      }
      if (PARAMS.indexOf(k) !== -1 && v) out[k] = limpiar(v);
    });
    return out;
  }

  function calcular() {
    var guardado = leerStorage();

    // Vencida: se descarta y se arranca de cero
    if (guardado.primera_visita) {
      var edad = Date.now() - new Date(guardado.primera_visita).getTime();
      if (edad > CFG.DIAS * 864e5) {
        log('atribución vencida, se descarta');
        guardado = {};
      }
    }

    var nuevos = deLaUrl();
    var hayNuevos = Object.keys(nuevos).length > 0;
    var hayGuardado = Object.keys(guardado).length > 0;

    // Sin parámetros nuevos: se mantiene lo que había
    if (!hayNuevos) {
      log('sin parámetros en la URL, se usa lo guardado:', guardado);
      return guardado;
    }

    // Con parámetros nuevos: decide el modelo de atribución
    if (hayGuardado && CFG.MODELO === 'primero') {
      log('ya había atribución y el modelo es "primero": no se pisa');
      return guardado;
    }

    nuevos.landing_inicial  = guardado.landing_inicial  || window.location.pathname;
    nuevos.referrer_inicial = guardado.referrer_inicial ||
                              (document.referrer ? limpiar(document.referrer) : 'directo');
    nuevos.primera_visita   = guardado.primera_visita   || new Date().toISOString();

    escribirStorage(nuevos);
    escribirCookie(nuevos);
    log('atribución capturada:', nuevos);
    return nuevos;
  }

  var ATRIBUCION = calcular();

  /* ================== INYECCIÓN EN FORMULARIOS ================== */

  /*
   * Se buscan los campos por CUATRO vías, porque cada plataforma deja
   * controlar cosas distintas:
   *
   *   1. [data-attr="gclid"]   HTML propio (control total)
   *   2. .attr-gclid           WordPress: WPForms, Fluent, Gravity y Elementor
   *                            dejan poner una clase CSS al campo, pero NO el
   *                            atributo name (WPForms lo genera como
   *                            wpforms[fields][7] y no se puede tocar).
   *   3. #attr-gclid           Elementor, que expone el ID del campo
   *   4. input[name="gclid"]   HTML simple y Contact Form 7
   *
   * Si el elemento encontrado es el contenedor (caso WPForms), se busca el
   * input adentro.
   */
  function inyectar() {
    var puestos = 0;

    TODOS.forEach(function (campo) {
      var valor = ATRIBUCION[campo] || '';
      var selector = [
        '[data-attr="' + campo + '"]',
        '.attr-' + campo,
        '#attr-' + campo,
        'input[name="' + campo + '"]'
      ].join(',');

      var nodos;
      try {
        nodos = document.querySelectorAll(selector);
      } catch (e) {
        return;
      }

      Array.prototype.forEach.call(nodos, function (nodo) {
        // Si no es un input, es el contenedor: buscar el input adentro
        var input = (nodo.tagName === 'INPUT' || nodo.tagName === 'TEXTAREA')
          ? nodo
          : nodo.querySelector('input, textarea');

        if (!input) return;
        if (input.value === valor) return;   // ya estaba, no tocar

        input.value = valor;

        // React, Vue y Alpine no se enteran de un cambio directo de .value:
        // hay que emitir los eventos a mano.
        try {
          input.dispatchEvent(new Event('input',  { bubbles: true }));
          input.dispatchEvent(new Event('change', { bubbles: true }));
        } catch (e) {
          // IE11
          var ev = document.createEvent('Event');
          ev.initEvent('change', true, true);
          input.dispatchEvent(ev);
        }
        puestos++;
      });
    });

    if (puestos) log('campos completados:', puestos);
    return puestos;
  }

  inyectar();

  /*
   * Los formularios que cargan por AJAX (multi-paso, popups, modales,
   * Elementor, forms que aparecen al hacer scroll) no existen todavía cuando
   * corre el script. El observador los completa cuando aparecen.
   * SIN ESTO, esos formularios llegan SIEMPRE VACÍOS: es el error más común
   * de esta implementación.
   */
  if (window.MutationObserver) {
    var pendiente = null;
    new MutationObserver(function () {
      // Se agrupan los cambios: sin esto, en páginas con mucho JS se
      // dispararía cientos de veces por segundo.
      clearTimeout(pendiente);
      pendiente = setTimeout(inyectar, 150);
    }).observe(document.documentElement, { childList: true, subtree: true });
  }

  // Red de seguridad: justo antes de enviar cualquier formulario se completa
  // otra vez. Cubre el caso del form que se arma en el mismo instante.
  document.addEventListener('submit', inyectar, true);

  /* ================== API PÚBLICA ================== */

  window.Atribucion = {
    // Objeto completo. Útil para armar el payload a mano.
    get: function () {
      var copia = {};
      TODOS.forEach(function (k) { copia[k] = ATRIBUCION[k] || ''; });
      copia.sitio = CFG.SITIO;
      return copia;
    },
    // Un solo campo: Atribucion.campo('utm_term')
    campo: function (k) { return ATRIBUCION[k] || ''; },
    // Volver a completar a mano si hiciera falta
    inyectar: inyectar,
    // Borrar lo guardado (para probar, o si el usuario retira el consentimiento)
    borrar: function () {
      try { window.localStorage.removeItem(CFG.CLAVE); } catch (e) {}
      document.cookie = CFG.CLAVE + '=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/';
      log('atribución borrada');
    },
    config: CFG
  };

  log('listo. Atribución activa:', window.Atribucion.get());

})(window, document);
