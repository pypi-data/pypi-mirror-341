import logging

import aiohttp
import asyncio

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DigitalHumanGenerator:
    def __init__(self):
        self.base_url = "https://vshow.guiji.ai"

    async def generate_digital_human(self, name, video_name, video_url, audio_url,
                                     app_id, secret_key, authorize_url, authorize_text):
        """Main method to generate a digital human"""
        logger.info(f"Starting digital human generation, name: {name}, video name: {video_name}")

        try:
            # 1. Get access token
            logger.info("Step 1: Getting access token...")
            token_data = await self.get_token(app_id, secret_key)
            access_token = token_data['data']['access_token']

            logger.info("Successfully obtained access token")

            # 2. Create metadata
            logger.info("Step 2: Creating metadata...")
            meta_data = await self.create_meta(access_token, name, video_url, authorize_url, authorize_text)
            training_id = meta_data['data']['trainingId']
            logger.info(f"Metadata created successfully, training_id: {training_id}")

            # 3. Get metadata status and wait for completion
            logger.info("Step 3: Waiting for metadata processing...")
            meta_result = await self.get_meta(access_token, training_id)
            scene_id = meta_result['data']['sceneId']
            logger.info(f"Metadata processing completed, scene_id: {scene_id}")

            # 4. Create video
            logger.info("Step 4: Creating video...")
            video_data = await self.create_video(access_token, scene_id, video_name, audio_url)
            video_id = video_data['data']['videoId']
            logger.info(f"Video created successfully, video_id: {video_id}")

            # 5. Get video status and wait for completion
            logger.info("Step 5: Waiting for video synthesis...")
            video_result = await self.get_video(access_token, video_id)
            final_video_url = video_result['data']['videoUrl']
            logger.info(f"Video synthesis completed, URL: {final_video_url}")
            return final_video_url

        except Exception as e:
            logger.error(f"Error occurred during digital human generation: {str(e)}")
            raise

    async def get_token(self, app_id, secret_key):
        """Get access token from the API"""
        url = f"{self.base_url}/partneropenapi/openapi/coze/oauth/token"
        payload = {
            "appId": app_id,
            "secretKey": secret_key
        }
        logger.debug(f"Requesting token, URL: {url}")
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as response:
                result = await response.json()
                if result.get('success'):
                    return result
                else:
                    error_msg = f"Failed to get token: {result.get('message', 'Unknown error')}"
                    logger.error(error_msg)
                    raise Exception(error_msg)

    async def create_meta(self, access_token, name, video_url, authorize_url, authorize_text):
        """Create metadata for digital human"""
        url = f"{self.base_url}/partneropenapi/openapi/coze/video/v2/create/training"
        payload = {
            "access_token": access_token,
            "authorizeText": authorize_text,
            "authorizeUrl": authorize_url,
            "level": "1",
            "name": name,
            "videoUrl": video_url
        }
        logger.debug(f"Creating metadata, URL: {url}")
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as response:
                result = await response.json()
                if result.get('success'):
                    return result
                else:
                    error_msg = f"Failed to create metadata: {result.get('message', 'Unknown error')}"
                    logger.error(error_msg)
                    raise Exception(error_msg)

    async def get_meta(self, access_token, training_id):
        """Get metadata status and wait for completion"""
        url = f"{self.base_url}/partneropenapi/openapi/coze/video/v2/training/get"
        payload = {
            "access_token": access_token,
            "id": training_id
        }

        attempt = 1
        while True:
            logger.debug(f"Checking metadata status, attempt {attempt}")
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as response:
                    result = await response.json()
                    if not result.get('success'):
                        error_msg = f"Failed to get metadata status: {result.get('message', 'Unknown error')}"
                        logger.error(error_msg)
                        raise Exception(error_msg)

                    status = result['data']['status']
                    logger.info(f"Current metadata status: {status}")

                    if status == 2:  # Success
                        return result
                    elif status in [0, 1]:  # Processing
                        logger.info("Metadata is being processed, retrying in 10 seconds...")
                        await asyncio.sleep(10)
                        attempt += 1
                        continue
                    else:  # Error
                        error_msg = f"Metadata processing failed, status code: {status}"
                        logger.error(error_msg)
                        raise Exception(error_msg)

    async def create_video(self, access_token, scene_id, video_name, audio_url):
        """Create video with the digital human"""
        url = f"{self.base_url}/partneropenapi/openapi/coze/video/v2/simpleCreate"
        payload = {
            "access_token": access_token,
            "audioUrl": audio_url,
            "sceneId": scene_id,
            "videoName": video_name
        }
        logger.debug(f"Creating video, URL: {url}")
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as response:
                result = await response.json()
                if result.get('success'):
                    return result
                else:
                    error_msg = f"Failed to create video: {result.get('message', 'Unknown error')}"
                    logger.error(error_msg)
                    raise Exception(error_msg)

    async def get_video(self, access_token, video_id):
        """Get video status and wait for completion"""
        url = f"{self.base_url}/partneropenapi/openapi/coze/video/v2/get"
        payload = {
            "access_token": access_token,
            "id": video_id
        }

        attempt = 1
        while True:
            logger.debug(f"Checking video status, attempt {attempt}")
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as response:
                    result = await response.json()
                    if not result.get('success'):
                        error_msg = f"Failed to get video status: {result.get('message', 'Unknown error')}"
                        logger.error(error_msg)
                        raise Exception(error_msg)

                    status = result['data']['synthesisStatus']
                    logger.info(f"Current video synthesis status: {status}")

                    if status == 3:  # Success
                        return result
                    elif status in [-1, 1, 2]:  # Processing
                        logger.info("Video is being synthesized, retrying in 10 seconds...")
                        await asyncio.sleep(10)
                        attempt += 1
                        continue
                    else:  # Error
                        error_msg = f"Video synthesis failed, status code: {status}"
                        logger.error(error_msg)
                        raise Exception(error_msg)


# Example usage
async def main():
    try:
        generator = DigitalHumanGenerator()
        video_url = await generator.generate_digital_human(
            name="test_name",
            video_name="test_video",
            video_url="https://cdn.guiji.ai/video-server/mp4/1906680038862909442.mp4",
            audio_url="https://digital-public-dev.obs.cn-east-3.myhuaweicloud.com/11/502279huanglichen.wav",
            app_id="tv9N2abqCfx0uSrp",
            secret_key="F501fW7d93K96u5Qb48p0RYhDx9wuLuXHmez4Y1Aj8cLPkwwj",
            authorize_url="https://cdn.guiji.ai/video-server/mp4/1906680038862909442.mp4",
            authorize_text="I am XXX, I authorize..."
        )
        logger.info(f"Digital human generation successful! Final video URL: {video_url}")

    except Exception as e:
        logger.error(f"Program execution error: {str(e)}")
        raise


if __name__ == "__main__":
    asyncio.run(main())