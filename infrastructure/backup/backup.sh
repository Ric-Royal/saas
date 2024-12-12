#!/bin/bash

# Load environment variables
source .env

# Set backup directory
BACKUP_DIR="/backups"
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup directory if it doesn't exist
mkdir -p $BACKUP_DIR

# Backup PostgreSQL databases
echo "Backing up PostgreSQL databases..."

# Public Participation
PGPASSWORD=$POSTGRES_PASSWORD pg_dump -h pp-db -U postgres -d public_participation > $BACKUP_DIR/public_participation_$DATE.sql

# BillBot
PGPASSWORD=$POSTGRES_PASSWORD pg_dump -h billbot-db -U postgres -d billbot > $BACKUP_DIR/billbot_$DATE.sql

# Agricultural Insights
PGPASSWORD=$POSTGRES_PASSWORD pg_dump -h agri-db -U postgres -d agri_insights > $BACKUP_DIR/agri_insights_$DATE.sql

# Backup MongoDB databases
echo "Backing up MongoDB databases..."

# CivilBot
mongodump --host civilbot-db --port 27017 --db civilbot --out $BACKUP_DIR/civilbot_$DATE

# Tech Blog
mongodump --host tech-blog-db --port 27018 --db tech_blog --out $BACKUP_DIR/tech_blog_$DATE

# Backup Neo4j database
echo "Backing up Neo4j database..."
neo4j-admin backup --backup-dir=$BACKUP_DIR/neo4j_$DATE --name=graph.db

# Compress backups
echo "Compressing backups..."
cd $BACKUP_DIR
tar -czf backups_$DATE.tar.gz *_$DATE*

# Upload to S3
echo "Uploading to S3..."
aws s3 cp backups_$DATE.tar.gz s3://$BACKUP_S3_BUCKET/

# Clean up old backups
echo "Cleaning up old backups..."
find $BACKUP_DIR -type f -mtime +$BACKUP_RETENTION_DAYS -delete

echo "Backup completed successfully!" 