module.exports = function(grunt) {

  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),

    imagemin: {
      media: {
        files: [{
          expand: true,
          cwd: 'media/images/',
          src: '{,*/}*.{png,jpg,jpeg,gif}',
          dest: 'media/images'
        }]
      }
    },

    watch: {
      sass: {
        files: "publichealth/static/**/*.scss",
        tasks: ['sass:dev']
      }
    },

    // TODO: switch to https://github.com/sindresorhus/grunt-sass
    sass: {                              // Task
      dev: {                            // Target
        options: {                       // Target options
          style: 'expanded',
          sourcemap: 'none'
        },
        files: {                         // Dictionary of files
          "./assets/css/main.css": "publichealth/static/css/main.scss"
        }
      },
      dist: {
        options: {
          style: 'compressed',
          sourcemap: 'none'
        },
        files: {
          "./assets/css/main.min.css": "publichealth/static/css/main.scss"
        }
      }
    },

    bgShell: {
      _defaults: {
        bg: true,
        stdout: false,
        stderr: false,
      },
      runDjango: {
        cmd: 'python manage.py runserver'
      },
    },

    browserSync: {
      dev: {
        bsFiles: {
          src: [
            "./assets/css/*.css",
            "./*.html"
          ]
        },
        options: {
          watchTask: true,
          proxy:  "localhost:8000"
        }
      }
    }
  });

  grunt.loadNpmTasks('grunt-contrib-imagemin');
  grunt.loadNpmTasks('grunt-contrib-sass');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-bg-shell');
  grunt.loadNpmTasks('grunt-browser-sync');
  grunt.registerTask('default', ['imagemin', 'sass']);
  grunt.registerTask('browser-sync', [
    'bgShell',
    'browserSync',
    'watch'
  ]);
};
