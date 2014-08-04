# -*- coding: utf-8 -*-

import logging
import requests
try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse
import copy

__version__ = '0.1a'

class InvalidModifier(ValueError):
    def __init__(self, msg):
        self.msg = msg
        
    def __unicode__(self):
        return self.msg

    
class ZKillboard(object):
    """ZKillboard API interface
    
    ZKillboard is a chain-able class, allowing for modifiers to be passed as a
    function chain as well as arguments on the `get` call.
    
    Arguments:
       base_url (str): Base API URL of the ZKB instance you want to use (defaults to zkillboard.com).
       modifier_validation (bool): Enables the modifier validation functions.
       user_agent (str): User agent to use when calling the API.
    
    """

    _MODIFIER_DATA = (
        ('limit', True),
        ('page', True),
        ('starttime', True),
        ('endtime', True),
        ('year', True),
        ('month', True),
        ('week', True),
        ('beforekillid', True),
        ('afterkillid', True),
        ('pastseconds', True),
        ('killid', True),
        ('kills', False),
        ('losses', False),
        ('w-space', False),
        ('solo', False),
        ('orderdirection', True),
        ('characterid', True),
        ('corporationid', True),
        ('allianceid', True),
        ('factionid', True),
        ('shiptypeid', True),
        ('groupid', True),
        ('solarsystemid', True),
        ('no-items', False),
        ('no-attackers', False),
        ('api-only', False),
        ('xml', False),
    )
    
    _MODIFIERS = [x for x, y in _MODIFIER_DATA]
    _MODIFIERS_ARGUMENT = [x for x, y in _MODIFIER_DATA if y]

    def __init__(self, base_url='https://zkillboard.com/api/', modifier_validation=True, user_agent='pyZKB %s' % __version__):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._base_url = base_url
        self._modifiers = []
        self._modifier_validation = modifier_validation
        self._xml_format = False
        self._user_agent = user_agent
        
    def __getattr__(self, name):
        def modifier_func(args=None):
            mod_name = name.replace('_', '-')
            if self._modifier_validation:
                if not mod_name.lower() in ZKillboard._MODIFIERS:
                    raise InvalidModifier('%s is a unknown modifier' % mod_name)
                if args is None and mod_name.lower() in ZKillboard._MODIFIERS_ARGUMENT:
                    raise InvalidModifier('%s requires a argument' % mod_name)
                if args and isinstance(args, list) and len(args) > 10:
                    raise ValueError('No more than 10 IDs are allowed at a time')
            x = copy.deepcopy(self)
            x._modifiers.append((mod_name, args))
            if mod_name.lower() == 'xml':
                x._xml_format = True
            return x
        return modifier_func
        
    def __deepcopy__(self, memo):
        x = self.__class__()
        x._base_url = copy.copy(self._base_url)
        x._modifiers = copy.deepcopy(self._modifiers)
        x._modifier_validation = copy.copy(self._modifier_validation)
        x._user_agent = copy.copy(self._user_agent)
        return x
        
    def get(self, **kwargs):
        """Calls the ZKB API with the modifiers specified
        
        Arguments:
           **kwargs: Additional modifiers
           
        Returns:
           tuple: (headers, result)
           
        Raises:
           ValueError: If the modifier has been provided an invalid values.
           InvalidModifier: If the modifier doesn't exist or is incorrectly used.
           
        Examples:
        
           Modifiers can be provided directly to the `get` call.
        
           >>> x = ZKillboard()
           >>> x.get(killID=12345)
           
           Or provided as part of a chained call for the class
           
           >>> x = ZKillboard()
           >>> x.killID(12345).get()
           
        """ 
        if len(kwargs):
            self._modifiers.extend(kwargs.items())
        url = self._construct_url(self._modifiers)
        self._logger.debug('Calling %s' % url)
        return self._get_url(url)
        
    def _construct_url(self, modifiers):
        url = ''
        for mod, val in modifiers:
            url += '%s/' % mod
            if val:
                if isinstance(val, list):
                    val = ','.join(val)
                url += '%s/' % val
        return urlparse.urljoin(self._base_url, url)
        
    def _get_url(self, url):
        headers = {
            'User-Agent': self._user_agent,
        }
        req = requests.get(url, headers=headers)
        if not req.status_code == requests.codes.ok:
            req.raise_for_status()
        if self._xml_format:
            return req.headers, req.text
        return req.headers, req.json()

