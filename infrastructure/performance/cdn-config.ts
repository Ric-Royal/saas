import { S3Client, PutObjectCommand } from '@aws-sdk/client-s3';
import { CloudFrontClient, CreateInvalidationCommand } from '@aws-sdk/client-cloudfront';
import { createHash } from 'crypto';

export class CDNManager {
  private s3Client: S3Client;
  private cloudfront: CloudFrontClient;
  private bucket: string;
  private distribution: string;

  constructor(config: {
    region: string;
    bucket: string;
    distribution: string;
    accessKeyId: string;
    secretAccessKey: string;
  }) {
    this.s3Client = new S3Client({
      region: config.region,
      credentials: {
        accessKeyId: config.accessKeyId,
        secretAccessKey: config.secretAccessKey,
      },
    });

    this.cloudfront = new CloudFrontClient({
      region: config.region,
      credentials: {
        accessKeyId: config.accessKeyId,
        secretAccessKey: config.secretAccessKey,
      },
    });

    this.bucket = config.bucket;
    this.distribution = config.distribution;
  }

  // Upload asset to S3 and return CDN URL
  async uploadAsset(
    file: Buffer,
    path: string,
    contentType: string
  ): Promise<string> {
    const hash = createHash('md5').update(file).digest('hex');
    const key = `${path}/${hash}`;

    await this.s3Client.send(
      new PutObjectCommand({
        Bucket: this.bucket,
        Key: key,
        Body: file,
        ContentType: contentType,
        CacheControl: 'public, max-age=31536000', // 1 year
      })
    );

    return `https://${this.distribution}.cloudfront.net/${key}`;
  }

  // Invalidate CDN cache
  async invalidateCache(paths: string[]): Promise<void> {
    await this.cloudfront.send(
      new CreateInvalidationCommand({
        DistributionId: this.distribution,
        InvalidationBatch: {
          CallerReference: Date.now().toString(),
          Paths: {
            Quantity: paths.length,
            Items: paths.map(p => p.startsWith('/') ? p : `/${p}`),
          },
        },
      })
    );
  }

  // Generate optimized image variants
  async generateImageVariants(
    imageBuffer: Buffer,
    path: string
  ): Promise<Record<string, string>> {
    const variants = {
      original: await this.uploadAsset(imageBuffer, path, 'image/jpeg'),
      thumbnail: await this.uploadAsset(
        await this.resizeImage(imageBuffer, 150),
        `${path}/thumbnail`,
        'image/jpeg'
      ),
      medium: await this.uploadAsset(
        await this.resizeImage(imageBuffer, 800),
        `${path}/medium`,
        'image/jpeg'
      ),
    };

    return variants;
  }

  // Helper method to resize images
  private async resizeImage(buffer: Buffer, width: number): Promise<Buffer> {
    const sharp = require('sharp');
    return sharp(buffer)
      .resize(width, null, {
        withoutEnlargement: true,
        fit: 'inside',
      })
      .jpeg({ quality: 80 })
      .toBuffer();
  }

  // Get CDN URL for a path
  getCDNUrl(path: string): string {
    return `https://${this.distribution}.cloudfront.net/${path}`;
  }

  // Check if asset exists in CDN
  async assetExists(path: string): Promise<boolean> {
    try {
      await this.s3Client.send(
        new PutObjectCommand({
          Bucket: this.bucket,
          Key: path,
        })
      );
      return true;
    } catch (error) {
      return false;
    }
  }
} 