#!/bin/bash
# Backup do estado insubstituível do Estúdio YouTube (ordem do Conselho, 17/07)
D=/opt/automacao/marcas/opoder/youtube
DEST=/root/bak_youtube_estado
mkdir -p "$DEST"
STAMP=$(date +%Y%m%d)
tar -czf "$DEST/estado_$STAMP.tar.gz" -C "$D" data pipeline.json frontend/capas 2>/dev/null
# retém 14 dias
find "$DEST" -name "estado_*.tar.gz" -mtime +14 -delete
