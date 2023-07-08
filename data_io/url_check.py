import re

class ChannelExtraction:
    def __init__(self, patterns):
        self.patterns = patterns

    def is_video_link(self, url):
        pattern = r"(?:https?:\/\/)?(?:www\.)?youtube\.com\/watch\?v=([A-Za-z0-9_-]+)"
        match = re.search(pattern, url)
        if match:
            channel_id = match.group(1)
            return channel_id, True
        return None,False

    def is_channel_link(self, url):
        pattern = r"(?:https?:\/\/)?(?:www\.)?youtube\.com\/(?:c\/|channel\/|user\/)?([a-zA-Z0-9\-_]+)"
        if re.match(pattern, url):
            channel_id_match = re.search(r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/(?:c\/|channel\/|user\/)?([a-zA-Z0-9\-_]+)', url)
            channel_name = channel_id_match.group(1)
            return channel_name, True
        return None,False

    def extract_channel(self, url):
        for pattern in self.patterns:
            match = re.search(pattern, url)
            if match:
                uri_style = match.group(1)
                return uri_style
        
        output,video_link = self.is_video_link(url)
        if video_link:
            return output
        
        output, channel_link = self.is_channel_link(url)
        if channel_link:
            return output
        
        pattern = r"(?:https|http)\:\/\/(?:[\w]+\.)?youtube\.com\/(?:c\/|channel\/|user\/)?([a-zA-Z0-9\-]{1,})"
        match = re.search(pattern, url)
        if match:
            return match.group(1)

        return None




    # url = "https://chat.openai.com/"
def check_url(url):
    patterns = [
        r"(?:\/(c)\/([%\d\w_\-]+)(\/.*)?)",
        r"(?:\/(channel)\/([%\w\d_\-]+)(\/.*)?)",
        r"(?:\/(u)\/([%\d\w_\-]+)(\/.*)?)",
        r"(?:\/(user)\/([%\w\d_\-]+)(\/.*)?)",
        r"(?:\/(@[%\w\d_\-]+)(\/.*)?)"
    ]
    channel_extractor = ChannelExtraction(patterns)
    output = channel_extractor.extract_channel(url)
    return output