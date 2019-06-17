# -*- coding: utf8 -*-


DOWNLOAD_URL_PATTERNS = {
    'macos': 'https://fastdl.mongodb.org/osx/mongodb-osx-ssl-x86_64-{version}.tgz'
}



if __name__ == '__main__':
    print(DOWNLOAD_URL_PATTERNS['macos'].format(version='4.0.10'))
