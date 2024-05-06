/*!
 *(https://getbootstrap.com/docs/5.3/customize/color-modes/#dark-mode)
 *Adaptation from bootstrap color modes JavaScript code.
 */

(() => {
  'use strict'

  const getStoredTheme = () => localStorage.getItem('theme')
  const setStoredTheme = theme => localStorage.setItem('theme', theme)

  const getPreferredTheme = () => {
    const storedTheme = getStoredTheme()
    if (storedTheme) {
      return storedTheme
    }

    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
  }

  const setTheme = theme => {
    if (theme === 'auto' && window.matchMedia('(prefers-color-scheme: dark)').matches) {
      document.documentElement.setAttribute('data-bs-theme', 'dark')
    } else {
      document.documentElement.setAttribute('data-bs-theme', theme)
    }
  }

  setTheme(getPreferredTheme())

  document.addEventListener('DOMContentLoaded', function() {
    if (document.documentElement.getAttribute('data-bs-theme') == 'light') {
        document.querySelector("#btnSwitch").textContent = 'Dark'
    }
    else {
        document.querySelector("#btnSwitch").textContent = 'Light'
    }

    document.documentElement.setAttribute('data-bs-theme', getStoredTheme())

    document.getElementById('btnSwitch').addEventListener('click',()=>{
      if (document.documentElement.getAttribute('data-bs-theme') == 'dark') {
          document.documentElement.setAttribute('data-bs-theme','light')
          document.querySelector("#btnSwitch").textContent = 'Dark'

          setStoredTheme("light")
      }
      else {
          document.documentElement.setAttribute('data-bs-theme','dark')
          document.querySelector("#btnSwitch").textContent = 'Light'

          setStoredTheme("dark")
      }
    });

  });

})();
