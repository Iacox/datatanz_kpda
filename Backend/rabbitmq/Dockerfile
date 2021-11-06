FROM rabbitmq:3-management

# Define environment variables.
ENV RABBITMQ_USER user1
ENV RABBITMQ_PASSWORD password1
ENV RABBITMQ_PID_FILE /var/lib/rabbitmq/mnesia/rabbitmq

ADD init.sh /init.sh
RUN chmod +x /init.sh
EXPOSE 15672

# Define default command
CMD ["/init.sh"]
