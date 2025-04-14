import os

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(24)
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload size
    UPLOAD_FOLDER = 'uploads'
    RESULTS_FOLDER = 'results'
    
    # ForgeTube resources paths
    SCRIPTS_PATH = "resources/scripts/"
    IMAGES_PATH = "resources/images/"
    AUDIO_PATH = "resources/audio/"
    FONT_PATH = "resources/font/font.ttf"
    
    # Default video settings
    DEFAULT_DURATION = 60  # in seconds
    MAX_DURATION = 300  # 5 minutes max
    
    # UI Settings
    ACCENT_COLOR = "#6366F1"  # Indigo
    DARK_BG = "#121212"
    DARKER_BG = "#0A0A0A"
    TEXT_COLOR = "#E5E7EB"
    
class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False
    
class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = False
    TESTING = True
    
class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    
config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}

def get_config():
    """Return the appropriate configuration object based on environment variable"""
    env = os.environ.get('FLASK_ENV', 'development')
    return config_by_name[env] 