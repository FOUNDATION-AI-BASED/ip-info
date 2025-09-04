[< Back to README](../README.md)

# Troubleshooting

This section provides solutions to common issues you might encounter while using or self-hosting the `ip-info` service.

## Common Issues

### 1. API Service Not Starting

**Symptoms**:
- API container fails to start
- Error messages about missing dependencies

**Solutions**:
1. Verify all dependencies are installed by running:
   ```bash
   pip install -r api/requirements.txt
   ```
2. Check Docker logs for specific errors:
   ```bash
   docker logs ip-info-api
   ```

### 2. MaxMind Database Issues

**Symptoms**:
- "Database not found" errors
- Outdated or incorrect geographical information

**Solutions**:
1. Ensure the updater service is running and has proper permissions
2. Verify the `.env` file contains correct `MAXMIND_LICENSE_KEY`
3. Manually trigger database update:
   ```bash
   docker-compose run updater
   ```

### 3. UI Not Loading

**Symptoms**:
- Blank page or errors in browser console
- UI container not responding

**Solutions**:
1. Check if UI container is running:
   ```bash
   docker ps
   ```
2. Rebuild UI assets if needed:
   ```bash
   docker-compose build ui
   ```

## Logging

To investigate issues, check these log locations:

- **API Service**:
  ```bash
  docker logs ip-info-api
  ```

- **UI Service**:
  ```bash
  docker logs ip-info-ui
  ```

- **Updater Service**:
  ```bash
  docker logs ip-info-updater
  ```

For more detailed debugging, you can increase log verbosity by setting `LOG_LEVEL=DEBUG` in your `.env` file.