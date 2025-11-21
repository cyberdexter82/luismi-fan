

/**
 * Módulo de Audio - Gestiona la reproducción de música
 */
const AudioModule = {
    /**
     * Inicializa el reproductor de audio personalizado en todas las canciones
     * Reemplaza el reproductor estándar HTML5 con controles personalizados
     */
    init() {
      // Esperar a que el DOM esté completamente cargado
      document.addEventListener('DOMContentLoaded', () => {
        // Buscar todos los elementos de audio en la página
        const audioElements = document.querySelectorAll('audio');
        
        // Si no hay elementos de audio, no continuar
        if (audioElements.length === 0) return;
        
        // Para cada elemento de audio, crear un reproductor personalizado
        audioElements.forEach((audio, index) => {
          // Obtener información de la canción del DOM
          const songContainer = audio.closest('.cancion');
          if (!songContainer) return;
          
          const songInfo = songContainer.querySelector('.cancion-info');
          const songTitle = songInfo ? songInfo.querySelector('.cancion-titulo').textContent : `Canción ${index + 1}`;
          
          // Crear contenedor para el reproductor personalizado
          const playerContainer = document.createElement('div');
          playerContainer.className = 'custom-player';
          playerContainer.innerHTML = `
            <div class="player-controls">
              <button class="play-button" title="Reproducir"><i class="fas fa-play"></i></button>
              <div class="progress-container">
                <div class="progress-bar"></div>
              </div>
              <span class="time-display">0:00 / 0:00</span>
              <button class="volume-button" title="Volumen"><i class="fas fa-volume-up"></i></button>
              <div class="volume-slider-container">
                <input type="range" class="volume-slider" min="0" max="1" step="0.05" value="1">
              </div>
              <button class="favorite-button" title="Añadir a favoritos" data-song="${songTitle}">
                <i class="far fa-heart"></i>
              </button>
            </div>
          `;
          
          // Reemplazar el reproductor estándar con nuestro reproductor personalizado
          audio.controls = false; // Desactivar los controles estándar
          audio.parentNode.insertBefore(playerContainer, audio.nextSibling);
          
          // Configurar los eventos para el reproductor personalizado
          this.setupPlayerEvents(audio, playerContainer);
        });
        
        // Inicializar el estado de los botones de favoritos
        this.updateFavoriteButtons();
      });
    },
    
    /**
     * Configura los eventos para el reproductor de audio personalizado
     * @param {HTMLAudioElement} audio - El elemento de audio a controlar
     * @param {HTMLElement} playerContainer - El contenedor del reproductor personalizado
     */
    setupPlayerEvents(audio, playerContainer) {
      const playButton = playerContainer.querySelector('.play-button');
      const progressContainer = playerContainer.querySelector('.progress-container');
      const progressBar = playerContainer.querySelector('.progress-bar');
      const timeDisplay = playerContainer.querySelector('.time-display');
      const volumeButton = playerContainer.querySelector('.volume-button');
      const volumeSlider = playerContainer.querySelector('.volume-slider');
      const favoriteButton = playerContainer.querySelector('.favorite-button');
      const songTitle = favoriteButton.dataset.song;
      
      // Evento de reproducción/pausa
      playButton.addEventListener('click', () => {
        if (audio.paused) {
          // Pausar todos los demás audios primero
          document.querySelectorAll('audio').forEach(a => {
            if (a !== audio && !a.paused) {
              a.pause();
              const otherButton = a.nextElementSibling.querySelector('.play-button i');
              if (otherButton) otherButton.className = 'fas fa-play';
            }
          });
          
          audio.play();
          playButton.querySelector('i').className = 'fas fa-pause';
        } else {
          audio.pause();
          playButton.querySelector('i').className = 'fas fa-play';
        }
      });
      
      // Actualizar la barra de progreso durante la reproducción
      audio.addEventListener('timeupdate', () => {
        const progress = (audio.currentTime / audio.duration) * 100;
        progressBar.style.width = `${progress}%`;
        
        // Actualizar el tiempo mostrado
        const currentMinutes = Math.floor(audio.currentTime / 60);
        const currentSeconds = Math.floor(audio.currentTime % 60).toString().padStart(2, '0');
        const totalMinutes = Math.floor(audio.duration / 60) || 0;
        const totalSeconds = Math.floor(audio.duration % 60).toString().padStart(2, '0') || '00';
        
        timeDisplay.textContent = `${currentMinutes}:${currentSeconds} / ${totalMinutes}:${totalSeconds}`;
      });
      
      // Permitir hacer clic en la barra de progreso para cambiar la posición
      progressContainer.addEventListener('click', (e) => {
        const rect = progressContainer.getBoundingClientRect();
        const clickPosition = (e.clientX - rect.left) / rect.width;
        audio.currentTime = clickPosition * audio.duration;
      });
      
      // Controlar el volumen
      volumeButton.addEventListener('click', () => {
        const volumeContainer = playerContainer.querySelector('.volume-slider-container');
        volumeContainer.style.display = volumeContainer.style.display === 'block' ? 'none' : 'block';
      });
      
      volumeSlider.addEventListener('input', () => {
        audio.volume = volumeSlider.value;
        // Actualizar el icono según el nivel de volumen
        const volumeIcon = volumeButton.querySelector('i');
        if (audio.volume === 0) {
          volumeIcon.className = 'fas fa-volume-mute';
        } else if (audio.volume < 0.5) {
          volumeIcon.className = 'fas fa-volume-down';
        } else {
          volumeIcon.className = 'fas fa-volume-up';
        }
      });
      
      // Gestionar favoritos
      favoriteButton.addEventListener('click', () => {
        const isFavorite = FavoritesModule.toggleFavorite(songTitle);
        favoriteButton.querySelector('i').className = isFavorite ? 'fas fa-heart' : 'far fa-heart';
      });
      
      // Reiniciar reproductor cuando termina la canción
      audio.addEventListener('ended', () => {
        progressBar.style.width = '0%';
        playButton.querySelector('i').className = 'fas fa-play';
      });
    },
    
    /**
     * Actualiza el estado de los botones de favoritos basado en localStorage
     */
    updateFavoriteButtons() {
      const favoriteButtons = document.querySelectorAll('.favorite-button');
      favoriteButtons.forEach(button => {
        const songTitle = button.dataset.song;
        const isFavorite = FavoritesModule.isFavorite(songTitle);
        button.querySelector('i').className = isFavorite ? 'fas fa-heart' : 'far fa-heart';
      });
    }
  };
  
  /**
   * Módulo de Favoritos - Gestiona el almacenamiento de canciones favoritas
   */
  const FavoritesModule = {
    /**
     * Clave utilizada para guardar favoritos en localStorage
     */
    STORAGE_KEY: 'luismiFan_favorites',
    
    /**
     * Obtiene la lista de favoritos de localStorage
     * @returns {Array} - Array con los títulos de las canciones favoritas
     */
    getFavorites() {
      const favoritesJson = localStorage.getItem(this.STORAGE_KEY);
      return favoritesJson ? JSON.parse(favoritesJson) : [];
    },
    
    /**
     * Guarda la lista de favoritos en localStorage
     * @param {Array} favorites - Array con los títulos de las canciones favoritas
     */
    saveFavorites(favorites) {
      localStorage.setItem(this.STORAGE_KEY, JSON.stringify(favorites));
    },
    
    /**
     * Verifica si una canción está en favoritos
     * @param {string} songTitle - Título de la canción
     * @returns {boolean} - true si la canción está en favoritos, false en caso contrario
     */
    isFavorite(songTitle) {
      const favorites = this.getFavorites();
      return favorites.includes(songTitle);
    },
    
    /**
     * Añade o elimina una canción de favoritos
     * @param {string} songTitle - Título de la canción
     * @returns {boolean} - true si se añadió, false si se eliminó
     */
    toggleFavorite(songTitle) {
      const favorites = this.getFavorites();
      const index = favorites.indexOf(songTitle);
      
      if (index === -1) {
        favorites.push(songTitle);
        this.showNotification(`"${songTitle}" añadida a favoritos`);
        this.saveFavorites(favorites);
        return true;
      } else {
        favorites.splice(index, 1);
        this.showNotification(`"${songTitle}" eliminada de favoritos`);
        this.saveFavorites(favorites);
        return false;
      }
    },
    
    /**
     * Muestra una notificación temporal en la pantalla
     * @param {string} message - Mensaje a mostrar
     */
    showNotification(message) {
      // Crear el elemento de notificación si no existe
      let notification = document.querySelector('.favorites-notification');
      if (!notification) {
        notification = document.createElement('div');
        notification.className = 'favorites-notification';
        document.body.appendChild(notification);
      }
      
      // Mostrar el mensaje
      notification.textContent = message;
      notification.classList.add('show');
      
      // Ocultar después de 2 segundos
      setTimeout(() => {
        notification.classList.remove('show');
      }, 2000);
    },
    
    /**
     * Inicializa la funcionalidad de favoritos
     */
    init() {
      document.addEventListener('DOMContentLoaded', () => {
        // Si estamos en la página de música disponible, añadir el botón de mostrar favoritos
        if (document.querySelector('.albumes-grid')) {
          const section = document.querySelector('.info-seccion');
          const favoritesButton = document.createElement('button');
          favoritesButton.className = 'boton-mini favorites-toggle';
          favoritesButton.style.margin = '1rem 0';
          favoritesButton.textContent = 'Mostrar mis favoritos';
          
          section.insertBefore(favoritesButton, section.querySelector('h2').nextSibling);
          
          // Crear contenedor para mostrar favoritos
          const favoritesContainer = document.createElement('div');
          favoritesContainer.className = 'favorites-container';
          favoritesContainer.style.display = 'none';
          section.insertBefore(favoritesContainer, favoritesButton.nextSibling);
          
          // Evento para mostrar/ocultar favoritos
          favoritesButton.addEventListener('click', () => {
            if (favoritesContainer.style.display === 'none') {
              favoritesContainer.style.display = 'block';
              favoritesButton.textContent = 'Ocultar mis favoritos';
              this.displayFavorites(favoritesContainer);
            } else {
              favoritesContainer.style.display = 'none';
              favoritesButton.textContent = 'Mostrar mis favoritos';
            }
          });
        }
      });
    },
    
    /**
     * Muestra las canciones favoritas en el contenedor específico
     * @param {HTMLElement} container - Contenedor para mostrar favoritos
     */
    displayFavorites(container) {
      const favorites = this.getFavorites();
      
      if (favorites.length === 0) {
        container.innerHTML = '<p>Aún no tienes canciones favoritas. Haz clic en el corazón junto a una canción para añadirla.</p>';
        return;
      }
      
      let html = '<h3>Mis canciones favoritas</h3><ul class="favorites-list">';
      favorites.forEach(song => {
        html += `<li class="favorite-item">
          <span>${song}</span>
          <button class="remove-favorite" data-song="${song}">
            <i class="fas fa-times"></i>
          </button>
        </li>`;
      });
      html += '</ul>';
      
      container.innerHTML = html;
      
      // Añadir evento para eliminar favoritos
      container.querySelectorAll('.remove-favorite').forEach(button => {
        button.addEventListener('click', () => {
          const songTitle = button.dataset.song;
          this.toggleFavorite(songTitle);
          this.displayFavorites(container);
          AudioModule.updateFavoriteButtons();
        });
      });
    }
  };
  
  /**
   * Módulo de Tema - Gestiona el cambio entre tema claro y oscuro
   */
  const ThemeModule = {
    /**
     * Clave para almacenar la preferencia de tema en localStorage
     */
    THEME_KEY: 'luismiFan_theme',
    
    /**
     * Inicializa el selector de tema
     */
    init() {
      document.addEventListener('DOMContentLoaded', () => {
        // Crear el botón de cambio de tema
        const header = document.querySelector('header .logo');
        const themeToggle = document.createElement('button');
        themeToggle.className = 'theme-toggle';
        themeToggle.innerHTML = '<i class="fas fa-moon"></i>';
        themeToggle.title = 'Cambiar tema';
        
        // Insertar el botón en el header
        header.appendChild(themeToggle);
        
        // Verificar tema guardado y aplicarlo
        const savedTheme = localStorage.getItem(this.THEME_KEY);
        if (savedTheme === 'dark') {
          document.body.classList.add('dark-theme');
          themeToggle.innerHTML = '<i class="fas fa-sun"></i>';
        }
        
        // Evento de cambio de tema
        themeToggle.addEventListener('click', () => {
          document.body.classList.toggle('dark-theme');
          const isDark = document.body.classList.contains('dark-theme');
          
          localStorage.setItem(this.THEME_KEY, isDark ? 'dark' : 'light');
          themeToggle.innerHTML = isDark ? '<i class="fas fa-sun"></i>' : '<i class="fas fa-moon"></i>';
        });
      });
    }
  };
  
  /**
   * Módulo de Búsqueda - Permite filtrar álbumes y canciones
   */
  const SearchModule = {
    /**
     * Inicializa la funcionalidad de búsqueda
     */
    init() {
      document.addEventListener('DOMContentLoaded', () => {
        // Solo añadir la búsqueda en la página de música disponible
        if (document.querySelector('.albumes-grid')) {
          // Crear el cuadro de búsqueda
          const section = document.querySelector('.info-seccion');
          const searchContainer = document.createElement('div');
          searchContainer.className = 'search-container';
          searchContainer.innerHTML = `
            <input type="text" class="search-input" placeholder="Buscar álbumes o canciones...">
            <button class="search-button"><i class="fas fa-search"></i></button>
          `;
          
          // Insertar antes del grid de álbumes
          section.insertBefore(searchContainer, section.querySelector('h2').nextSibling);
          
          // Evento de búsqueda
          const searchInput = searchContainer.querySelector('.search-input');
          searchInput.addEventListener('input', () => {
            this.performSearch(searchInput.value);
          });
          
          // Limpiar búsqueda al hacer clic en el botón
          const searchButton = searchContainer.querySelector('.search-button');
          searchButton.addEventListener('click', () => {
            searchInput.value = '';
            this.performSearch('');
          });
        }
        
        // Añadir búsqueda en la página de detalles de álbum
        if (document.querySelector('.canciones-lista')) {
          const cancionesLista = document.querySelector('.canciones-lista');
          const searchContainer = document.createElement('div');
          searchContainer.className = 'search-container';
          searchContainer.innerHTML = `
            <input type="text" class="search-input" placeholder="Filtrar canciones...">
            <button class="search-button"><i class="fas fa-search"></i></button>
          `;
          
          // Insertar antes de la lista de canciones
          cancionesLista.insertBefore(searchContainer, cancionesLista.querySelector('h3').nextSibling);
          
          // Evento de búsqueda
          const searchInput = searchContainer.querySelector('.search-input');
          searchInput.addEventListener('input', () => {
            this.filterSongs(searchInput.value);
          });
          
          // Limpiar búsqueda al hacer clic en el botón
          const searchButton = searchContainer.querySelector('.search-button');
          searchButton.addEventListener('click', () => {
            searchInput.value = '';
            this.filterSongs('');
          });
        }
      });
    },
    
    /**
     * Realiza la búsqueda en los álbumes
     * @param {string} query - Texto de búsqueda
     */
    performSearch(query) {
      const albums = document.querySelectorAll('.album-card');
      query = query.toLowerCase().trim();
      
      albums.forEach(album => {
        const title = album.querySelector('h3').textContent.toLowerCase();
        const description = album.querySelector('p:nth-child(3)').textContent.toLowerCase();
        
        if (title.includes(query) || description.includes(query)) {
          album.style.display = '';
        } else {
          album.style.display = 'none';
        }
      });
      
      // Mostrar mensaje si no hay resultados
      let noResultsMessage = document.querySelector('.no-results-message');
      const visibleAlbums = Array.from(albums).filter(album => album.style.display !== 'none');
      
      if (visibleAlbums.length === 0 && query !== '') {
        if (!noResultsMessage) {
          noResultsMessage = document.createElement('p');
          noResultsMessage.className = 'no-results-message';
          noResultsMessage.textContent = 'No se encontraron álbumes que coincidan con tu búsqueda.';
          document.querySelector('.albumes-grid').after(noResultsMessage);
        }
      } else if (noResultsMessage) {
        noResultsMessage.remove();
      }
    },
    
    /**
     * Filtra las canciones en la vista de detalles del álbum
     * @param {string} query - Texto de búsqueda
     */
    filterSongs(query) {
      const songs = document.querySelectorAll('.cancion');
      query = query.toLowerCase().trim();
      
      songs.forEach(song => {
        const title = song.querySelector('.cancion-titulo').textContent.toLowerCase();
        
        if (title.includes(query)) {
          song.style.display = '';
        } else {
          song.style.display = 'none';
        }
      });
      
      // Mostrar mensaje si no hay resultados
      let noResultsMessage = document.querySelector('.no-results-message');
      const visibleSongs = Array.from(songs).filter(song => song.style.display !== 'none');
      
      if (visibleSongs.length === 0 && query !== '') {
        if (!noResultsMessage) {
          noResultsMessage = document.createElement('p');
          noResultsMessage.className = 'no-results-message';
          noResultsMessage.textContent = 'No se encontraron canciones que coincidan con tu búsqueda.';
          document.querySelector('.canciones-lista').appendChild(noResultsMessage);
        }
      } else if (noResultsMessage) {
        noResultsMessage.remove();
      }
    }
  };
  
  /**
   * App principal - Inicializa todos los módulos
   */
  const App = {
    /**
     * Inicializa la aplicación
     */
    init() {
      // Inicializar módulos
      AudioModule.init();
      FavoritesModule.init();
      ThemeModule.init();
      SearchModule.init();
      
      // Inicializar Vue en páginas específicas
      this.initVueComponents();
    },
    
    /**
     * Inicializa los componentes de Vue
     */
    initVueComponents() {
      document.addEventListener('DOMContentLoaded', () => {
        // Verificar si estamos en la página principal
        if (document.querySelector('.datos-curiosos')) {
          // Inicializar el contador de visitas
          this.initVisitCounter();
        }
        
        // Si estamos en la página de detalles de un álbum, inicializar el componente de calificación
        if (document.querySelector('.album-detalle')) {
          this.initRatingComponent();
        }
      });
    },
    
    /**
     * Inicializa el contador de visitas en Vue
     */
    initVisitCounter() {
      // Crear el contenedor para el componente Vue
      const infoDestacado = document.querySelector('.info-destacado');
      const counterContainer = document.createElement('div');
      counterContainer.id = 'visit-counter';
      infoDestacado.appendChild(counterContainer);
      
      // Crear la aplicación Vue
      new Vue({
        el: '#visit-counter',
        data: {
          visits: parseInt(localStorage.getItem('luismiFan_visits') || '0')
        },
        created() {
          // Incrementar contador de visitas
          this.visits++;
          localStorage.setItem('luismiFan_visits', this.visits);
        },
        template: `
          <div class="visit-counter-container">
            <h3>Tu contador de visitas</h3>
            <p>Has visitado esta página {{ visits }} {{ visits === 1 ? 'vez' : 'veces' }}</p>
          </div>
        `
      });
    },
    
    /**
     * Inicializa el componente de calificación del álbum
     */
    initRatingComponent() {
      // Obtener el título del álbum
      const albumTitle = document.querySelector('.album-info-detalle h2').textContent;
      const storageKey = `luismiFan_rating_${albumTitle.replace(/\s+/g, '_')}`;
      
      // Crear el contenedor para el componente Vue
      const albumInfo = document.querySelector('.album-info-detalle');
      const ratingContainer = document.createElement('div');
      ratingContainer.id = 'album-rating';
      albumInfo.appendChild(ratingContainer);
      
      // Crear la aplicación Vue
      new Vue({
        el: '#album-rating',
        data: {
          rating: parseInt(localStorage.getItem(storageKey) || '0'),
          tempRating: 0,
          albumTitle
        },
        methods: {
          setRating(value) {
            this.rating = value;
            localStorage.setItem(storageKey, value);
          },
          setTempRating(value) {
            this.tempRating = value;
          },
          resetTempRating() {
            this.tempRating = 0;
          }
        },
        computed: {
          displayRating() {
            return this.tempRating || this.rating;
          }
        },
        template: `
          <div class="album-rating">
            <p>¿Te gusta este álbum? ¡Califícalo!</p>
            <div class="rating-stars">
              <span
                v-for="n in 5"
                :key="n"
                :class="['star', { 'filled': n <= displayRating }]"
                @click="setRating(n)"
                @mouseover="setTempRating(n)"
                @mouseleave="resetTempRating()"
              >★</span>
            </div>
            <p v-if="rating > 0">Tu calificación: {{ rating }} de 5</p>
          </div>
        `
      });
    }
  };
  
  // Inicializar la aplicación
  App.init();