#!/bin/bash

# Actualizar paquetes y agregar soporte para locales
apt-get update && apt-get install -y locales && locale-gen es_ES.UTF-8

# Exportar el locale para que Python lo use
export LANG=es_ES.UTF-8
export LC_ALL=es_ES.UTF-8
